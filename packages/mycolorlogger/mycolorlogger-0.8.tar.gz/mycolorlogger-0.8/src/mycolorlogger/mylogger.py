import logging
import time
import sys
import colorlog
def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class log():
    def __init__(self):
        self.logger = colorlog.getLogger()
        self.logger.setLevel(colorlog.colorlog.logging.INFO)
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] [%(levelname)s] %(white)s%(message)s', datefmt='%H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bg_red',
            },
            secondary_log_colors={},
            style='%'))
        self.logger.addHandler(handler)

# from Mylogger import log
# log.logger.debug("Debug message")
# log.logger.info("Information message")
# log.logger.warning("Warning message")
# log.logger.error("Error message")
# log.logger.critical("Critical message")
