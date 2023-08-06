import configparser
import os
from . import constutlis


# file_path = "E:/var/app-config/sshapp-cost-config/application.server.properties"
# file = open(file_path, 'r', encoding="GBK")
# file_content = file.read()
# file_content = "[default]\n" + file_content


def get_ini_value(file: str, section: str, key: str, encoding=constutlis.CHARSET_UTF_8) -> str:
    """
    读取ini配置文件的一个配置值
    注意：ini配置文件的key需要小写，因为这里会把大写的key全部转为小写

    :param file: 配置文件
    :param section: key所属组
    :param key: key
    :param encoding: 编码
    :return:
    """
    if not os.path.isfile(file):
        raise ValueError("读取配置文件夹失败，配置文件不存在, 参数:" + file)
    config = configparser.ConfigParser()
    config.read(file, encoding)
    return config.get(section, key)


def get_ini_section_values(file: str, section: str, encoding=constutlis.CHARSET_UTF_8) -> dict:
    """
    读取ini配置文件的一个组的配置值
    注意：ini配置文件的key需要小写，因为这里会把大写的key全部转为小写
    """
    if not os.path.isfile(file):
        raise ValueError("读取配置文件夹失败，配置文件不存在, 参数:" + file)
    config = configparser.ConfigParser()
    config.read(file, encoding)
    items = config.items(section)
    return dict(items)


def get_ini_values(file: str, encoding=constutlis.CHARSET_UTF_8) -> dict:
    """
    读取ini配置文件的所有的配置值
    注意：ini配置文件的key需要小写，因为这里会把大写的key全部转为小写
    """
    if not os.path.isfile(file):
        raise ValueError("读取配置文件夹失败，配置文件不存在, 参数:" + file)
    config = configparser.ConfigParser()
    config.read(file, encoding)
    result = {}
    sections = config.sections()
    for section in sections:
        result.update(get_ini_section_values(file, section, encoding))
    return result


def get_properties_value(file: str, key: str, encoding=constutlis.CHARSET_UTF_8) -> str:
    """
    读取properties配置文件的一个配置值

    :param file: 配置文件
    :param key: key
    :param encoding: 编码
    """
    if not os.path.isfile(file):
        raise ValueError("读取配置文件夹失败，配置文件不存在, 参数:" + file)
    file_object = None
    try:
        file_object = open(file, mode="r", encoding=encoding)
        lines = file_object.readlines()
        value = None
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.startswith("="):
                raise ValueError("读取配置文件夹失败，配置文件配置错误, 配置项:" + line)
            splits = line.split("=", 1)
            if len(splits) != 2:
                raise ValueError("读取配置文件夹失败，配置文件配置错误, 配置项:" + line)
            if splits[0].strip() == key.strip():
                value = splits[1]
                break
        return value
    finally:
        if file_object:
            file_object.close()


def get_properties_values(file: str, encoding=constutlis.CHARSET_UTF_8) -> dict:
    """
    读取properties配置文件的所有配置值

    :param file: 配置文件
    :param encoding: 编码
    """
    if not os.path.isfile(file):
        raise ValueError("读取配置文件夹失败，配置文件不存在, 参数:" + file)
    file_object = None
    try:
        file_object = open(file, mode="r", encoding=encoding)
        lines = file_object.readlines()
        values = {}
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.startswith("="):
                raise ValueError("读取配置文件夹失败，配置文件配置错误, 配置项:" + line)
            splits = line.split("=", 1)
            if len(splits) != 2:
                raise ValueError("读取配置文件夹失败，配置文件配置错误, 配置项:" + line)
            values.update({splits[0]: splits[1]})
        return values
    finally:
        if file_object:
            file_object.close()
