import datetime
from dataclasses import dataclass


@dataclass
class ExpireTime:
    hour: int
    minute: int
    second: int

    def future_date(self):
        now = datetime.datetime.now()
        target_date = datetime.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
        )

        if now.hour == self.hour and now.minute == self.minute and now.second == self.second:
            return target_date.replace(day=now.day + 1)

        elif target_date > now:
            return target_date

        return target_date.replace(day=now.day + 1)
