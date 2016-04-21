# coding:UTF-8


"""
日志模块
@author: yubang
2016.04.21
"""


from logging.handlers import TimedRotatingFileHandler
import logging


formatter = logging.Formatter('%(name)-12s %(asctime)s level-%(levelname)-8s thread-%(thread)-8d %(message)s')
fileTimeHandler = TimedRotatingFileHandler("log/app.log", "D", 1, 0)
fileTimeHandler.suffix = "%Y%m%d.log"
fileTimeHandler.setFormatter(formatter)

log = logging.getLogger('app_log')
log.setLevel(logging.INFO)
log.addHandler(fileTimeHandler)
