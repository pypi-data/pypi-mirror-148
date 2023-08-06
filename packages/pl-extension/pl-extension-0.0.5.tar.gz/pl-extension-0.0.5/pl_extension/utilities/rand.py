import time

__all__ = ["time_string"]


def time_string(short=False) -> str:
    """
    Return time as string, used as random string
    """
    year = time.localtime().tm_year
    mon = time.localtime().tm_mon
    day = time.localtime().tm_mday
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    sec = time.localtime().tm_sec
    if short:
        return "%02d%02d%02d" % (hour, min, sec)
    else:
        return "%04d%02d%02d_%02d%02d%02d" % (year, mon, day, hour, min, sec)
