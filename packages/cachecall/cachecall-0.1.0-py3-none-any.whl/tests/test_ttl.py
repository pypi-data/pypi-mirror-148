import time

from cachecall import cache
from unittest.mock import Mock


class TestCacheWithTTL:
    def test_cache_ttl(self):
        inner = Mock()
        inner.side_effect = [1, 2, 3]

        @cache(ttl=1)
        def func(x=None):
            return inner()

        call_1 = func()
        call_2 = func()

        assert inner.call_count == 1
        assert call_1 == 1
        assert call_2 == 1

        time.sleep(1)

        call_3 = func()
        call_4 = func()

        assert inner.call_count == 2
        assert call_3 == 2
        assert call_4 == 2

        call_4 = func(1)

        assert inner.call_count == 3
        assert call_4 == 3
