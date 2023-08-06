import os

"""
 系统相关的工具方法
"""


def is_windows() -> bool:
    """
    是否是widows系统

    :return:
    """
    # 返回系统类型： nt是windows操作系统, posix是Linux系统
    system_type = os.name
    if system_type == "nt":
        return True
    else:
        return False


def is_linux() -> bool:
    """
    是否是Linux系统

    :return:
    """
    return not is_windows()


def get_system_envs() -> dict:
    """
    获取所有的系统环境变量

    :return: 所有的系统环境变量
    """
    environ = os.environ
    environ_dict = dict(environ)
    return environ_dict


def get_system_env_value(env_name: str) -> str:
    """
    获取系统环境变量值

    :param env_name: 环境变量名
    :return: 环境变量值
    """
    environ = os.environ
    return environ.get(env_name)
