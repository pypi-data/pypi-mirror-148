"""
 日期、时间相关的工具方法
"""
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from datetime import tzinfo
from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import timezone
from . import constutlis


class DateTimeFormatter:
    """
    日期时间格式化器
    """

    def __init__(self, formatter_str: str) -> None:
        self.__formatter_str = formatter_str

    @property
    def formatter_str(self) -> str:
        return self.__formatter_str


class DateFormatter:
    """
    日期格式化器
    """

    def __init__(self, formatter_str: str) -> None:
        self.__formatter_str = formatter_str

    @property
    def formatter_str(self) -> str:
        return self.__formatter_str


"""
常用的日期时间格式化器
"""
#
DateTimeFormatter_DATETIME = DateTimeFormatter(constutlis.DATETIME_FORMAT_DATETIME)
#
DateTimeFormatter_DATE = DateTimeFormatter(constutlis.DATETIME_FORMAT_DATE)

"""
常用的日期格式化器
"""
#
DateFormatter_DATE = DateFormatter(constutlis.DATETIME_FORMAT_DATE)


def get_now() -> datetime:
    """
    获取当前日期时间
    """
    return datetime.now()


def format_datetime(datetime_obj: datetime, formatter: DateTimeFormatter) -> str:
    """
    将日期时间对象(datetime类型)转换成字符串\n
    :param datetime_obj:
    :param formatter:
    :return:
    """
    if not isinstance(datetime_obj, datetime):
        raise ValueError("格式化时间失败，参数错误：参数不是datetime类型")
    if not isinstance(formatter, DateTimeFormatter):
        raise ValueError("格式化时间失败，参数错误：参数不是DateTimeFormatter类型")
    return datetime_obj.strftime(formatter.formatter_str)


def parse_datetime(datetime_str: str, formatter: DateTimeFormatter) -> datetime:
    """
    将日期时间字符串转换成datetime对象\n
    1.datetime_str格式需要与formatter参数格式一致\n
    2.如果datetime_str只有日期，没有时间，则转换出来的时间都是0填充\n
    :param datetime_str:
    :param formatter:
    :return:
    """
    return datetime.strptime(datetime_str, formatter.formatter_str)


def get_now_date():
    """
    获取当前日期
    """
    return date.today()


def format_date(date_obj: date, formatter: DateFormatter) -> str:
    """
    将日期时间对象(datetime类型)转换成字符串\n
    :param date_obj:
    :param formatter:
    :return:
    """
    if not isinstance(date_obj, date):
        raise ValueError("格式化时间失败，参数错误：参数不是date类型")
    if not isinstance(formatter, DateFormatter):
        raise ValueError("格式化时间失败，参数错误：参数不是DateFormatter类型")
    return date_obj.strftime(formatter.formatter_str)


def parse_date(date_str: str, formatter: DateFormatter) -> date:
    """
    将日期时间字符串转换成date对象\n
    1.datetime_str格式需要与formatter参数格式一致\n
    :param date_str:
    :param formatter:
    :return:
    """
    datetime_obj = parse_datetime(date_str, DateTimeFormatter(formatter.formatter_str))
    date_obj = date(datetime_obj.year, datetime_obj.month, datetime_obj.day)
    return date_obj
