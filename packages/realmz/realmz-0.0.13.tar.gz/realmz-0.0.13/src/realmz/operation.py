import calendar
from datetime                               import datetime


class Operation:

    @staticmethod
    def is_leap_year(year):
        return calendar.isleap(year)

    @staticmethod
    def get_today_date():
        return datetime.today().date()

    @staticmethod
    def str_to_date(str_date):
        if 'T' in str_date:
            return datetime.strptime(str_date.rsplit('T', 1)[0], "%Y-%m-%d").date()
        if '+' in str_date:
            return datetime.strptime(str_date.rsplit('+', 1)[0], "%Y-%m-%dT%H:%M:%S").date()
        elif ':' not in str_date:
            return datetime.strptime(str_date.rsplit('+', 1)[0], "%Y-%m-%d").date()
    