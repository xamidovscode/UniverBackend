import calendar
from datetime import datetime, timedelta


def get_last_day_of_month(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime(date.year, date.month, last_day)

def get_count_of_days(start_date, end_date):
    count = 0
    while start_date <= end_date:
        count += 1
        start_date += timedelta(days=1)
    return count