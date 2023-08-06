import logging
import os
from . import constutlis
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from logging import Formatter

"""
1.打印异常栈方式：logger.exception(baseException)， baseException为异常对象

"""

# 日志输出格式
LOG_FORMAT = "[%(asctime)s.%(msecs)d] [%(thread)s] [%(levelname)s] [%(name)s] %(module)s.%(funcName)s(%(lineno)d): %(message)s"
# 日志时间格式
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# 日志级别
LOG_DEFAULT_LEVEL = logging.INFO
# 是否打印到控制台
LOG_STD_OUT = True
# 是否写入到文件
LOG_FILE_OUT = True
# 日志文件路径，当为None或者""时,会输出到屏幕, 这里的路径是相对于工作路径的，而不是文件路径
LOG_FILE_DEFAULT_PAHT = "./logs/app.log"


def get_logger(logger_name: str, log_file_path=LOG_FILE_DEFAULT_PAHT) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    # 日志级别
    logger.setLevel(LOG_DEFAULT_LEVEL)
    # 日志输出格式
    formatter = Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    if LOG_STD_OUT:
        streamHandler = StreamHandler()
        streamHandler.setLevel(LOG_DEFAULT_LEVEL)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
    if LOG_FILE_OUT:
        # when:切割日志文件的时间单位
        # interval：切割日志文件的时间，即interval个when时间会切割日志文件
        # backupCount:保留日志个数, 过时自动删除
        if log_file_path is None or log_file_path == '':
            raise ValueError("需要配置日志文件位置")
        if not os.path.exists(os.path.abspath(os.path.dirname(log_file_path))):
            raise ValueError("配置的日志文件文件夹不存在, 日志文件夹：" + os.path.abspath(os.path.dirname(log_file_path)))
        file_handler = TimedRotatingFileHandler(log_file_path, encoding=constutlis.CHARSET_UTF_8, when="D",
                                                interval=10, backupCount=31)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(LOG_DEFAULT_LEVEL)
        logger.addHandler(file_handler)
    return logger
