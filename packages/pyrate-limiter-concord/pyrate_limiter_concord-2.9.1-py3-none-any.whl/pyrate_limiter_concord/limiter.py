from time import monotonic
from typing import Any, Callable, Dict, Type

from .bucket import RedisBucket
from .exceptions import BucketFullException, InvalidParams
from .request_rate import RequestRate


class Limiter:
    """Main rate-limiter class

    Args:
        rates: Request rate definitions
        bucket_class: Bucket backend to use; may be any subclass of :py:class:`.AbstractBucket`.
            See :py:mod`pyrate_limiter.bucket` for available bucket classes.
        bucket_kwargs: Extra keyword arguments to pass to the bucket class constructor.
        time_function: Time function that returns the current time as a float, in seconds
    """

    def __init__(
        self,
        *rates: RequestRate,
        bucket_class: Type[RedisBucket] = RedisBucket,
        bucket_kwargs: Dict[str, Any] = None,
        time_function: Callable[[], float] = None,
    ):
        self._validate_rate_list(rates)
        self._rates = rates
        self._bkclass = bucket_class
        self._bucket_args = bucket_kwargs or {}
        self.bucket_group: Dict[str, RedisBucket] = {}
        self.time_function = monotonic
        if time_function is not None:
            self.time_function = time_function
        # Call for time_function to make an anchor if required.
        self.time_function()

    def _validate_rate_list(self, rates):  # pylint: disable=no-self-use
        """Raise exception if rates are incorrectly ordered."""
        if not rates:
            raise InvalidParams("Rate(s) must be provided")

        for idx, rate in enumerate(rates[1:]):
            prev_rate = rates[idx]
            invalid = rate.limit <= prev_rate.limit or rate.interval <= prev_rate.interval
            if invalid:
                msg = f"{prev_rate} cannot come before {rate}"
                raise InvalidParams(msg)

    async def _init_buckets(self, identities) -> None:
        """Initialize a bucket for each identity, if needed.
        The bucket's maxsize equals the max limit of request-rates.
        """
        maxsize = self._rates[-1].limit
        for item_id in sorted(identities):
            if not self.bucket_group.get(item_id):
                self.bucket_group[item_id] = self._bkclass(
                    maxsize=maxsize,
                    identity=item_id,
                    **self._bucket_args,
                )
            self.bucket_group[item_id].lock_acquire()

    async def _release_buckets(self, identities) -> None:
        """Release locks after bucket transactions, if applicable"""
        for item_id in sorted(identities):
            self.bucket_group[item_id].lock_release()

    async def acquire(self, *client_ip: str) -> None:
        """Attempt to acquire an item, or raise an error if a rate limit has been exceeded.

        Args:
            identities: One or more identities to acquire. Typically this is the name of a service
                or resource that is being rate-limited.

        Raises:
            :py:exc:`BucketFullException`: If the bucket is full and the item cannot be acquired
        """
        await self._init_buckets(client_ip)
        now = self.time_function()
        rate = self._rates[0]

        for item_id in client_ip:
            bucket = self.bucket_group[item_id]
            volume = await bucket.size()

            if volume < rate.limit:
                continue

            # Determine rate's starting point, and check requests made during its time window
            item_count, remaining_time = bucket.inspect_expired_items(now - rate.interval)
            if item_count >= rate.limit:
                await self._release_buckets(client_ip)
                raise BucketFullException(item_id, rate, remaining_time)

            # Remove expired bucket items beyond the last (maximum) rate limit,
            if rate is self._rates[-1]:
                await bucket.get(volume - item_count)

        # If no buckets are full, add another item to each bucket representing the next request
        for item_id in client_ip:
            await self.bucket_group[item_id].put(now)
        await self._release_buckets(client_ip)

    async def get_current_volume(self, client_ip: str) -> int:
        """Get current bucket volume for a specific identity"""
        bucket = self.bucket_group[client_ip]
        return await bucket.size()

    async def flush_all(self) -> int:
        cnt = 0

        for _, bucket in self.bucket_group.items():
            await bucket.flush()
            cnt += 1

        return cnt
