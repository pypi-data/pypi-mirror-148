from uuid import uuid4
from unittest.mock import Mock

from cachecall import cache, clear_cache


class TestCacheGroup:
    def test_different_groups(self):
        inner1 = Mock()
        inner2 = Mock()
        expected_result1 = ["a", "b", "c"]
        expected_result2 = [1, 2, 3]

        inner1.side_effect = expected_result1
        inner2.side_effect = expected_result2

        @cache()
        def func1(x=None):
            return inner1()

        @cache()
        def func2(x=None):
            return inner2()

        call_f1_1 = func1(x=1)
        call_f1_2 = func1(x=1)

        call_f2_1 = func2(x=1)
        call_f2_2 = func2(x=1)

        assert call_f1_1 == expected_result1[0]
        assert call_f1_2 == expected_result1[0]

        assert call_f2_1 == expected_result2[0]
        assert call_f2_2 == expected_result2[0]

    def test_same_group(self):
        inner1 = Mock()
        inner2 = Mock()
        expected_result1 = ["a", "b", "c"]
        expected_result2 = [1, 2, 3]

        inner1.side_effect = expected_result1
        inner2.side_effect = expected_result2

        @cache(group_name="default")
        def func1(x=None):
            return inner1()

        @cache(group_name="default")
        def func2(x=None):
            return inner2()

        call_f1_1 = func1(x=1)
        call_f1_2 = func1(x=1)
        call_f2_1 = func2(x=1)
        call_f2_2 = func2(x=1)

        assert call_f1_1 == expected_result1[0]
        assert call_f1_2 == expected_result1[0]
        assert call_f2_1 == expected_result2[0]
        assert call_f2_2 == expected_result2[0]

    def test_clear_cache_group(self):
        inner1 = Mock()
        expected_result1 = ["a", "b", "c"]

        inner1.side_effect = expected_result1

        group_name = str(uuid4())

        @cache(group_name=group_name)
        def func1(x=None):
            return inner1()

        func1(x=1)
        func1(x=1)

        assert inner1.call_count == 1

        clear_cache(group_name)

        func1(x=1)
        func1(x=1)

        assert inner1.call_count == 2
