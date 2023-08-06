import asyncio

from functools import wraps
from datetime import datetime


LOOP = asyncio.get_event_loop()


def get_hms_to_expire():
    now = datetime.now()
    minute = now.minute
    second = now.second + 1

    if second == 60:
        second = 0
        minute += 1

    return now.hour, minute, second


class MockDatetime:
    def __init__(self, now) -> None:
        self._now = now

    def now(self):
        return self._now

    def __call__(self, *args, **kwargs):
        return datetime(*args, **kwargs)


def run_async(coro):
    return LOOP.run_until_complete(coro)


def async_test(async_test_function):
    @wraps(async_test_function)
    def inner(*args, **kwargs):
        return run_async(async_test_function(*args, **kwargs))

    return inner


def pytest_sessionfinish(session, exitstatus):
    LOOP.close()
