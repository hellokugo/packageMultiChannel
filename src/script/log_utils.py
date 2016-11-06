'''
logging.DEBUG 输出一些琐碎的调试信息
logging.INFO 输出一些阶段性的标志
logging.WARNING 输出一些有可能出现问题的日志
logging.ERROR 输出异常
logging.CRITICAL 输出异常
'''
import logging
import sys
import platform
from PyQt4.QtCore import *

# 控制台输出的等级
STREAM_HANDLER_LEVEL = logging.DEBUG
# 文件输出的等级
FILE_HANDLER_LEVEL = logging.INFO
# 日志输出格式
LOG_FORMAT_STRING = '%(asctime)s [line %(lineno)d in %(filename)s - %(funcName)s] %(levelname)s : %(message)s'

class MyStreamHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self, stream=sys.stdout)
    def format(self, record):
        try:
            return logging.StreamHandler.format(self, record)
        except Exception as e:
            print(e);
        
class MyFileHandler(logging.FileHandler):
    def format(self, record):
        try:
            return logging.FileHandler.format(self, record)
        except Exception as e:
            print(e)

formatter = logging.Formatter(LOG_FORMAT_STRING)

logger = logging.getLogger('PackChannel')
logger.setLevel(logging.DEBUG)

mySH = MyStreamHandler()
mySH.setLevel(STREAM_HANDLER_LEVEL)
mySH.setFormatter(formatter)

logger.addHandler(mySH)

def getLogger():
    return logger

class SigalOutLogSender(QObject):
    def SendMsg(self, m):
        self.emit(SIGNAL('displayLog(QString)'),m)

aSigalOutLog=SigalOutLogSender()

class OutLog:
    def __init__(self):
        pass

    def write(self, m):
        global aSigalOutLog
        aSigalOutLog.SendMsg(u'%s ' % m)

sys.stdout = OutLog()
sys.stderr = OutLog()
