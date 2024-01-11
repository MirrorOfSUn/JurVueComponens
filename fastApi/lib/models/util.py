from datetime import datetime


def date2int(d: datetime | None = None) -> int:
    """
    Convert DateTime to int or return current date
    :param d: datetime or None(current datetime)
    :return: unix time
    """
    d = d or datetime.now()
    return int(d.timestamp() * 1000)


def int2date(i: int) -> datetime:
    """
    Convert Unix time to datetime
    :param i: unixtime
    :return: datetime
    """
    return datetime.fromtimestamp(i/1000)
