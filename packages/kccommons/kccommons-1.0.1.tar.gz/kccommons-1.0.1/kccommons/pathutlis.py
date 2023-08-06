"""
文件夹、文件路径相关的工具方法
"""
from os import path


def join_path(base_path: str, extend_path: str) -> str:
    """
    拼接路径

    :param base_path:路径
    :param extend_path:扩展路径，可以包含文件名，或者就只是文件名
    :return:
    """
    return path.join(base_path, extend_path)


def get_absolute_path(source_path: str) -> str:
    """
    获取绝对路径
    1.如果参数就是绝对路径，直接返回；
    2.如果参数是相对路径，则会根据当前的工作目录生成绝对路径返回；
    3.不管生成的绝对路径是否存在，都不会报错，并且都会有返回值

    :param source_path:
    """
    return path.abspath(source_path)


def is_absolute_path(source_path: str) -> bool:
    """
    是否是绝对路径
    1.如果参数是绝对路径，返回True；
    2.如果参数是相对路径，返回False；
    3.不管生成的绝对路径是否存在，都不会报错，并且都会有返回值

    :param source_path:
    """
    return path.isabs(source_path)


def get_base_path(source_path: str) -> str:
    """
     获取参数中最后一个斜杠之前的所有内容；
     如果参数是相对路径，返回的也是相对路径；
     如果参数是".",则返回的是""

    :param source_path:
    :return:
    """
    return path.dirname(source_path)


def get_base_name(source_path: str) -> str:
    """
     获取参数中最后一个斜杠之后的所有内容；
     如果参数是相对路径，返回的也是相对路径；
     如果参数是".",则返回的是""

    :param source_path:
    :return:
    """
    return path.basename(source_path)
