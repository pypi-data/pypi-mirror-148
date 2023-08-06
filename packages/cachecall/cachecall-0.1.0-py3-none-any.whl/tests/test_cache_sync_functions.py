from unittest.mock import Mock
from cachecall import cache


class TestCacheInSyncFunctions:
    def test_create_cache_with_func(self):
        m_inner_func = Mock()
        expected_result = 10
        m_inner_func.return_value = expected_result

        @cache(max_size_call=1)
        def func():
            return m_inner_func()

        call_one = func()
        call_two = func()

        assert call_one == expected_result
        assert call_two == expected_result
        assert m_inner_func.call_count == 1

    def test_create_caches(self):
        m_inner_func = Mock()
        results = [10, 20, 30, 40, 50]
        m_inner_func.side_effect = results

        @cache()
        def func(*args, **kwargs):
            return m_inner_func()

        call_1 = func(1)
        call_2 = func("1")
        call_3 = func(a=1)
        call_4 = func(2, a=1)
        call_5 = func(2, a=1)

        assert call_1 == results[0]
        assert call_2 == results[1]
        assert call_3 == results[2]
        assert call_4 == results[3]
        assert call_5 == results[3]

        assert m_inner_func.call_count == 4

    def test_create_cache_grather_than_max_size(self):
        m_inner_func = Mock()
        expected_result = [10, 20]
        m_inner_func.side_effect = expected_result

        @cache(max_size_call=1)
        def func(*args):
            return m_inner_func()

        call_one = func("a")
        call_two = func("b")
        call_three = func("b")

        assert call_one == expected_result[0]
        assert call_two == expected_result[1]
        assert call_three == expected_result[1]

        assert m_inner_func.call_count == 2

    def test_create_cache_with_key_no_cache(self):
        m_inner_func = Mock()
        expected_result = [10, 20]
        m_inner_func.side_effect = expected_result

        @cache(ignore_keys=["no_cache"])
        def func(arg, no_cache="abcd"):
            return m_inner_func()

        call_one = func("a", no_cache=1)
        call_two = func("a", no_cache="2 xyz")
        call_three = func("b", no_cache="abc")
        call_four = func("b", no_cache=5.5)

        assert call_one == expected_result[0]
        assert call_two == expected_result[0]
        assert call_three == expected_result[1]
        assert call_four == expected_result[1]
