from unittest.mock import Mock

from cachecall import cache
from tests.conftest import run_async


class TestCacheInAsyncFunctions:
    def test_create_cache_with_async_func(self):
        m_inner_func = Mock()
        expected_result = 10
        m_inner_func.return_value = expected_result

        @cache(max_size_call=1)
        async def func():
            return m_inner_func()

        call_one = run_async(func())
        call_two = run_async(func())

        assert call_one == expected_result
        assert call_two == expected_result
        assert m_inner_func.call_count == 1

    def test_create_async_cache_grather_than_max_size(self):
        m_inner_func = Mock()
        expected_result = [10, 20]
        m_inner_func.side_effect = expected_result

        @cache(max_size_call=1)
        async def func(*args):
            return m_inner_func()

        call_one = run_async(func("a"))
        call_two = run_async(func("b"))
        call_three = run_async(func("b"))

        assert call_one == expected_result[0]
        assert call_two == expected_result[1]
        assert call_three == expected_result[1]

        assert m_inner_func.call_count == 2
