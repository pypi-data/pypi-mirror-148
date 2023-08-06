from unittest.mock import Mock
from cachecall import cache, kb

from tests.fixtures.data import B1, B2


class TestCacheMemSize:
    def test_not_cache_big_data(self):
        inner = Mock()
        inner.return_value = B1

        @cache(max_size_mem=100)
        def func(x):
            return inner()

        func("a")
        func("a")
        func("a")

        assert inner.call_count == 3

    def test_cache_mem(self):
        func_b1 = Mock()
        func_b1.return_value = B1

        func_b2 = Mock()
        func_b2.return_value = B2

        @cache(max_size_mem=kb(2))
        def func(param):
            if param == "a":
                return func_b1()

            return func_b2()

        func("a")  # Add b1 in cache
        func("a")  # Use cache

        assert func_b1.call_count == 1

        func("b")  # Remove b1 data and add b2 in cache
        func("b")  # Use cache

        assert func_b2.call_count == 1

        func("a")  # Remove b2 data and add b1 in cache
        func("a")  # Use cache

        assert func_b1.call_count == 2

        func("b")  # Remove b1 data and add b2 in cache
        func("b")  # Use cache

        assert func_b2.call_count == 2
