import logging
import os, time
import colorlog
from Libraries.other_tools.setting import get_curr_path

# workdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# workdir = oget_curr_path())
LOG_PATH = os.path.join(get_curr_path(), "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

log_color_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bold'
}


class Logger:
    def __init__(self):
        self.log_name = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        self.file_format = logging.Formatter \
            ("[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s")
        self.console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] '
                ': %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_color_config
        )
        self.file_logger = logging.FileHandler(self.log_name, mode="w+", encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.console.setFormatter(self.console_formatter)
        self.file_logger.setLevel(logging.DEBUG)
        # self.file_logger.setFormatter(self.file_format)
        self.file_logger.setFormatter(self.file_format)

        self.logger.addHandler(self.console)
        self.logger.addHandler(self.file_logger)


logger = Logger().logger

if __name__ == "__main__":
    # logger.info("---测试开始---")
    # logger.debug("---测试结束---")
    # logger.error("---error info---")
    # logger.warning("---WARNING---")
    print(LOG_PATH)
