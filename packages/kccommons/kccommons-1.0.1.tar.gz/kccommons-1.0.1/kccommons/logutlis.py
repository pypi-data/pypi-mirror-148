import logging
import os

from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from logging import Formatter

from . import constutlis
from . import configutlis
from . import fileutlis
from . import dirutlis

"""
1.打印异常栈方式：logger.exception(baseException)， baseException为异常对象

"""

# 日志输出格式
LOG_FORMAT = "[%(asctime)s.%(msecs)d] [%(thread)s] [%(levelname)s] [%(name)s] %(module)s.%(funcName)s(%(lineno)d): %(message)s"
# 日志时间格式
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# 日志配置文件，放在项目的根目录下
LOG_FILE_CONFIG_PATH = "log.ini"


def get_logger(logger_name: str) -> logging.Logger:
    default_log_level = logging.INFO
    # 是否写入到文件
    default_log_file_out = False
    # 日志文件路径，当为None或者""时,会输出到屏幕, 这里的路径是相对于工作路径的，而不是文件路径
    default_log_file_path = "./logs/app.log"
    #
    if fileutlis.is_file_exists(LOG_FILE_CONFIG_PATH):
        # 日志等级
        loglevel = configutlis.get_ini_value(LOG_FILE_CONFIG_PATH, "log", "log.level")
        if loglevel is not None and loglevel.lower().strip() == "debug":
            default_log_level = logging.DEBUG
        elif loglevel is not None and loglevel.lower().strip() == "info":
            default_log_level = logging.INFO
        elif loglevel is not None and (loglevel.lower().strip() == "warn" or loglevel.lower().strip() == "warning"):
            default_log_level = logging.WARN
        elif loglevel is not None and loglevel.lower().strip() == "error":
            default_log_level = logging.ERROR
        elif loglevel is not None and (loglevel.lower().strip() == "fatal" or loglevel.lower().strip() == "critical"):
            default_log_level = logging.FATAL
        else:
            default_log_level = logging.INFO
        # 是否输出到文件
        logfileout = configutlis.get_ini_value(LOG_FILE_CONFIG_PATH, "log", "log.file.out")
        if logfileout is not None and logfileout.strip() != "" and logfileout.strip().lower() == "true":
            default_log_file_out = True
        # 日志文件路径
        logfilepath = configutlis.get_ini_value(LOG_FILE_CONFIG_PATH, "log", "log.file.path")
        if logfilepath is not None and logfilepath.strip() != "":
            default_log_file_path = logfilepath
    #
    logger = logging.getLogger(logger_name)
    # 日志级别
    logger.setLevel(default_log_level)
    # 日志输出格式
    formatter = Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    # 控制台输出
    streamHandler = StreamHandler()
    streamHandler.setLevel(default_log_level)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    if default_log_file_out:
        # when:切割日志文件的时间单位
        # interval：切割日志文件的时间，即interval个when时间会切割日志文件
        # backupCount:保留日志个数, 过时自动删除
        if not os.path.exists(os.path.abspath(os.path.dirname(default_log_file_path))):
            # raise ValueError("配置的日志文件文件夹不存在, 日志文件夹：" + os.path.abspath(os.path.dirname(default_log_file_path)))
            dirutlis.create_dirs(os.path.dirname(default_log_file_path))
        file_handler = TimedRotatingFileHandler(default_log_file_path, encoding=constutlis.CHARSET_UTF_8, when="D",
                                                interval=1, backupCount=31)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(default_log_level)
        logger.addHandler(file_handler)
    return logger
