from . import osutlis
from . import logutlis
from . import fileutlis
import subprocess
import time
import os
import psutil


class JvmParams:
    """
    JVM参数
    """
    __slots__ = ("__xms", "__xmx")

    def __init__(self, xms: str, xmx: str) -> None:
        """

        :param xms: 初始化JAVA堆的大小
        :param xmx: java堆的最大值
        """
        self.__xms = xms
        self.__xmx = xmx
        # assert unit and (unit.lower() == "m" or unit.lower() == "g"), "unit参数值只能为：'m' or 'M' or 'g' or 'G'"
        # assert xms and isinstance(xms, int) and xms > 0, "xms不能为空，且为正整数"
        # assert xmx and isinstance(xmx, int) and xmx > 0, "xmx不能为空，且为正整数"

    @property
    def xms(self) -> str:
        return self.__xms

    @property
    def xmx(self) -> str:
        return self.__xmx


class SpringBoot:
    @staticmethod
    def startup(jar_file_name: str, port: str, app_config_file_name: str, log_config_file_name: str,
                jvm_params: JvmParams):
        #
        assert jar_file_name is not None and jar_file_name.strip() != "", "请传入参数jar_path"
        assert port is not None and int(port) > 0, "请传入参数port,且port为正整数"
        assert app_config_file_name is not None and app_config_file_name.strip() != "", "请传入参数app_config_path"
        assert log_config_file_name is not None and log_config_file_name.strip() != "", "请传入参数log_config_path"
        assert jvm_params is not None, "请传入参数jvm_params"
        #
        path_prefix = os.path.join(os.getcwd(), "app")
        jar_path = os.path.join(path_prefix, jar_file_name)
        app_config_path = os.path.join(path_prefix, app_config_file_name)
        log_config_path = os.path.join(path_prefix, log_config_file_name)
        assert fileutlis.is_file_exists(jar_path), "jar包不存在：" + jar_path
        assert fileutlis.is_file_exists(app_config_path), "配置文件件不存在：" + app_config_path
        assert fileutlis.is_file_exists(log_config_path), "日志配置文件不存在：" + log_config_path
        if osutlis.is_windows():
            SpringBoot.startup_windows(jar_path, port, app_config_path, log_config_path, jvm_params)
        else:
            pass

    @staticmethod
    def startup_windows(jar_abspath: str, port: str, app_config_path: str, log_config_path: str, jvm_params: JvmParams):
        logger = logutlis.get_logger(__name__)
        # 判断端口号有没被占用
        with os.popen("netstat  -ano | findstr " + str(port)) as ret:
            lines = ret.readlines()
            assert lines is None or len(lines) <= 0, "服务已经启动、或端口号已经被占用:" + str(port) + "."
        # 判断程序是否已经启动
        with os.popen("jps  -l") as ret:
            lines = ret.readlines()
            assert len(list(filter(lambda item: item.find(jar_abspath) >= 0, lines))) <= 0, "启动失败，服务已经启动"
        # 启动jar
        app = subprocess.Popen([
            "start",
            "javaw",
            "-Xms" + jvm_params.xms,
            "-Xmx" + jvm_params.xmx,
            "-jar", jar_abspath,
            "--server.port=" + port,
            "--spring.config.location=" + app_config_path,
            "--logging.config=" + log_config_path,
        ],
            encoding="UTF-8", shell=True)
        begin_time = int(time.time())
        while True:
            logger.info("SpringBoot APP Starting...")
            end_time = int(time.time())
            has_jps = False
            # 判断启动进程是否存在
            with os.popen("jps  -l") as ret:
                lines = ret.readlines()
                for line in lines:
                    if line.find(jar_abspath) >= 0:
                        has_jps = True
                        break
            if not has_jps and (end_time - begin_time) > 15:
                logger.error("SpringBoot APP Start Fail!")
                return
                # 如果有端口号，则启动成功
            with os.popen("netstat  -ano | findstr " + str(port)) as ret:
                lines = ret.readlines()
                if lines is not None and len(lines) > 0:
                    logger.info("SpringBoot APP Start Success.")
                    break
            # 主线程休眠，再次循环判断, 单位：秒
            time.sleep(3)

    @staticmethod
    def shutdown(jar_file_name: str, port: str):
        #
        assert jar_file_name is not None and jar_file_name.strip() != "", "请传入参数jar_path"
        assert port is not None and int(port) > 0, "请传入参数port,且port为正整数"
        #
        path_prefix = os.path.join(os.getcwd(), "app")
        jar_abspath = os.path.join(path_prefix, jar_file_name)
        if osutlis.is_windows():
            SpringBoot.shutdown_windows(jar_abspath, port)
        else:
            pass

    @staticmethod
    def shutdown_windows(jar_abspath: str, port: str):
        logger = logutlis.get_logger(__name__)
        with os.popen("netstat  -ano | findstr " + str(port)) as ret:
            lines = ret.readlines()
            for line in lines:
                words = line.split()
                if words and words[1].endswith(":" + port):
                    pid = words[4].strip()
                    if psutil.pid_exists(int(pid)):
                        kill_command = "taskkill /f /t /im " + pid
                        with os.popen(kill_command) as kill_ret:
                            kill_ret.read()
        logger.info("SpringBoot APP Stop Success.")
