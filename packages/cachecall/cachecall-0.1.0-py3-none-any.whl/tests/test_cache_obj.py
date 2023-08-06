from datetime import datetime
from unittest import mock

from cachecall.cache import Cache
from cachecall import ExpireTime
from tests.conftest import MockDatetime


class TestCacheObject:
    @mock.patch("cachecall.expire_time.datetime")
    def test_expire_time_tuple(self, m_datetime):
        now = datetime.now()
        min_exp_date_expected = datetime(now.year, now.month, now.day, 12, 0, 0)
        m_datetime.datetime = MockDatetime(now=datetime(now.year, now.month, now.day, 10, 0, 0))
        expires_time = (ExpireTime(6, 0, 0), ExpireTime(12, 0, 0), ExpireTime(18, 0, 0))
        cache_obj = Cache(expire_time=expires_time)  # type: ignore

        assert cache_obj._expire_date() == min_exp_date_expected

    @mock.patch("cachecall.expire_time.datetime")
    def test_expire_time_list(self, m_datetime):
        now = datetime.now()
        min_exp_date_expected = datetime(now.year, now.month, now.day, 6, 0, 0)
        m_datetime.datetime = MockDatetime(now=datetime(now.year, now.month, now.day, 5, 59, 0))
        expires_time = (ExpireTime(6, 0, 0), ExpireTime(12, 0, 0))
        cache_obj = Cache(expire_time=expires_time)  # type: ignore

        assert cache_obj._expire_date() == min_exp_date_expected
