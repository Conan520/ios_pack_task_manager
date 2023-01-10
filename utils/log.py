import sys

from loguru import logger

log_file = "output.log"


class Logger:
    def __init__(self, log_file_path=log_file):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # 颜色>时间
                               # "{process.name} | "  # 进程名
                               "{thread.name} | "  # 线程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level:<8}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        enqueue=True,
                        )
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(log_file_path, level='DEBUG',
                        format='{time:YYYY-MM-DD HH:mm:ss} - '  # 时间
                               # "{process.name} | "  # 进程名
                               "{thread.name} | "  # 线程名
                               '{module}.{function}:{line} | {level:<8} : {message}',  # 模块名.方法名:行号
                        rotation="10 MB",
                        enqueue=True,
                        )

    def get_logger(self):
        return self.logger


log = Logger().get_logger()
