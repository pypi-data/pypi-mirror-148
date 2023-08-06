from typing import Tuple, Optional


def _remove_non_cached_property(kwargs: dict, ignore_keys: Optional[Tuple[str]]) -> dict:
    if not ignore_keys:
        return kwargs

    cache_kwargs = kwargs.copy()

    for key in kwargs.keys():
        if key in ignore_keys:
            del cache_kwargs[key]

    return cache_kwargs


def create_key(func_name: str, args: tuple, kwargs: dict, ignore_keys: Optional[Tuple[str]]) -> str:
    kwargs_to_cache = _remove_non_cached_property(kwargs, ignore_keys)

    if not args and not kwargs_to_cache:
        arg_key = "no-key"

    if args and kwargs_to_cache:
        arg_key = f"{str(args)}_{str(kwargs_to_cache)}"

    elif kwargs_to_cache:
        arg_key = str(kwargs_to_cache)

    else:
        arg_key = str(args)

    return f"{func_name}_{arg_key}"
