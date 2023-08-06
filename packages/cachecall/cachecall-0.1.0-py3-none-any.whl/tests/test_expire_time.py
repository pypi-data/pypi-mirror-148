from datetime import datetime
from cachecall.expire_time import ExpireTime
from tests.conftest import get_hms_to_expire


class TestExpireTime:
    def test_time_future_next_day(self):
        now = datetime.now()
        expected_next_day = now.day + 1

        hour = now.hour - 1
        minutes = 10
        seconds = 10

        tm = ExpireTime(hour, minutes, seconds)
        future_date = tm.future_date()

        assert future_date.day == expected_next_day
        assert future_date.minute == minutes
        assert future_date.second == seconds

    def test_time_future_self_day(self):
        now = datetime.now()

        h, m, s = get_hms_to_expire()

        tm = ExpireTime(h, m, s)
        future_date = tm.future_date()

        assert future_date.day == now.day
        assert future_date.minute == m
        assert future_date.second == s

    def test_time_future_equal_now(self):
        now = datetime.now()
        expected_day = now.day + 1

        tm = ExpireTime(now.hour, now.minute, now.second)
        future_date = tm.future_date()

        assert future_date.day == expected_day
        assert future_date.minute == now.minute
        assert future_date.second == now.second
