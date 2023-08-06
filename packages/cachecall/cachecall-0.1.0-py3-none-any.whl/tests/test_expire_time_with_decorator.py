import time
from unittest.mock import Mock

from cachecall import cache, ExpireTime
from tests.conftest import get_hms_to_expire


class TestExpireTimeDecorator:
    def test_expire_time(self):
        inner = Mock()
        inner.side_effect = [1, 2]

        h, m, s = get_hms_to_expire()

        @cache(expire_time=ExpireTime(h, m, s))
        def func():
            return inner()

        func()
        func()

        assert inner.call_count == 1

        time.sleep(1)
        func()

        assert inner.call_count == 2

    def test_expire_time_with_ttl(self):
        inner = Mock()
        inner.side_effect = [1, 2]

        h, m, s = get_hms_to_expire()

        @cache(expire_time=ExpireTime(h, m, s), ttl=2)
        def func():
            return inner()

        func()
        func()

        assert inner.call_count == 1

        time.sleep(1)
        func()

        assert inner.call_count == 2

    def test_many_expire_time(self):
        inner = Mock()
        inner.side_effect = [1, 2]

        h, m, s = get_hms_to_expire()

        @cache(
            expire_time=(
                ExpireTime(h, m, s),
                ExpireTime(h, m, s + 1),
            )  # type: ignore
        )
        def func():
            return inner()

        func()
        func()

        assert inner.call_count == 1

        time.sleep(1)
        func()

        assert inner.call_count == 2
