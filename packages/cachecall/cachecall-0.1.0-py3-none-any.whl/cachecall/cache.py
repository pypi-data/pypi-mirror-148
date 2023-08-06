from dataclasses import dataclass
from typing import Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from collections import OrderedDict

from cachecall.data import data
from cachecall.expire_time import ExpireTime


DEFAULT_GROUP = "default"


def clear_cache(group=DEFAULT_GROUP):
    if group in data:
        data[group] = OrderedDict()


@dataclass
class Cache:
    max_size_call: Optional[int] = 0
    group: str = DEFAULT_GROUP
    ttl: Optional[Union[int, float]] = None  # seconds
    expire_time: Optional[Union[ExpireTime, Tuple[ExpireTime]]] = None
    max_size_mem: Optional[Union[int, float]] = None  # bytes

    def _expire_date(self) -> Optional[datetime]:
        ttl_expiration = None

        if not self.ttl and not self.expire_time:
            return None

        if self.ttl:
            ttl_expiration = datetime.now() + timedelta(seconds=self.ttl)

        if self.ttl and not self.expire_time:
            return ttl_expiration

        if self.expire_time:
            if isinstance(self.expire_time, tuple) or isinstance(self.expire_time, list):
                expires_date = [et.future_date() for et in self.expire_time]

            else:
                expires_date = [self.expire_time.future_date()]

            if ttl_expiration:
                expires_date.append(ttl_expiration)

            return min(expires_date)

    def __post_init__(self):
        if self.group not in data:
            data[self.group] = OrderedDict()

        self.mem_usage = 0

    def set(self, key: str, value: Any):
        byte_size_of_value = value.__sizeof__()
        data[self.group][key] = {
            "value": value,
            "expires_at": self._expire_date(),
            "sizeof": byte_size_of_value,
        }
        self.mem_usage += byte_size_of_value

    def get(self, key: str) -> Optional[Any]:
        value_cached = data[self.group].get(key)

        if not value_cached:
            return None

        if value_cached.get("expires_at") and datetime.now() > value_cached["expires_at"]:
            del data[self.group][key]
            return None

        return value_cached.get("value")

    def is_full(self) -> bool:
        return self.max_size_call and len(data[self.group]) == self.max_size_call  # type: ignore

    def remove_first_item(self):
        removed_value_with_key = data[self.group].popitem(last=False)
        removed_value = removed_value_with_key[1]
        self.mem_usage -= removed_value["sizeof"]
        del removed_value_with_key

    @property
    def data(self):
        return data[self.group]

    def supported_mem_limit(self, value):
        return value.__sizeof__() <= self.max_size_mem

    def has_memory_space(self, value):
        return value.__sizeof__() + self.mem_usage <= self.max_size_mem
