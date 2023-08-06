import datetime
import time


def current_milli_time():
    return round(time.time() * 1000)


def datetime_iso_format(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def now_with_days_delta(days):
    return datetime.datetime.now() + datetime.timedelta(days=days)


def reset_to_midnight(value):
    return datetime_iso_format(value.replace(hour=0, minute=0, second=0, microsecond=0))
