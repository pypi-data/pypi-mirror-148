import inspect
import asyncio
import logging

from uuid import uuid4
from functools import wraps
from typing import Optional, Tuple, Union

from cachecall.cache import Cache
from cachecall.cache_keys import create_key
from cachecall.expire_time import ExpireTime


def cache(
    max_size_call: Optional[int] = None,
    group_name: Optional[str] = None,
    ttl: Optional[Union[int, float]] = None,
    expire_time: Optional[Union[ExpireTime, Tuple[ExpireTime]]] = None,
    ignore_keys: Optional[Tuple[str]] = None,
    max_size_mem: Optional[Union[int, float]] = None,  # bytes
    log_level: Optional[Union[str, int]] = logging.WARNING,
):
    def inner_cached(func):
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)  # type: ignore

        group = group_name if group_name else f"{func.__name__}_{str(uuid4())}"

        cache = Cache(max_size_call, group, ttl, expire_time, max_size_mem)

        @wraps(func)
        async def async_inner(*args, **kwargs):
            nonlocal ignore_keys
            nonlocal cache

            key = create_key(func.__name__, args, kwargs, ignore_keys)

            result = cache.get(key)

            if result:
                return result

            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if cache.is_full():
                cache.remove_first_item()

            if max_size_mem:
                number_checks = len(cache.data) + 1
                # + 1 -> because if the cached data was fully cleaned a next
                # iteration will be used for add data in cache (cache.set).
                # In below loop "for _ in range(number_checks)".

                if not cache.supported_mem_limit(result):
                    logger.debug(f"Data not cached. data bytes size is bigger than {max_size_mem}.")
                    return result

                for _ in range(number_checks):
                    if cache.has_memory_space(result):
                        cache.set(key, result)
                        break

                    logger.debug("Remove one data for clear memory space.")
                    cache.remove_first_item()
            else:
                cache.set(key, result)

            return result

        @wraps(func)
        def sync_inner(*args, **kwargs):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:  # pragma: no cover
                loop = asyncio.new_event_loop()

            return loop.run_until_complete(async_inner(*args, **kwargs))

        setattr(sync_inner, "cache", cache)
        setattr(async_inner, "cache", cache)

        if inspect.iscoroutinefunction(func):
            return async_inner

        return sync_inner

    return inner_cached
