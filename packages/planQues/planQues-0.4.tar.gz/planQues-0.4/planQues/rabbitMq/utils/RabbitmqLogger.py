import sys,logging,json,time
from logging import CRITICAL,FATAL,ERROR ,WARNING ,WARN ,INFO ,DEBUG ,NOTSET,_srcfile
from ai.common.log import LoggerFactory
from ai.utils.string_utils import exceptionNow2String
#项目地址: https://github.com/drudru/ansi_up
#解决方法(ansi)在网页中显示终端颜色
#前端将后端返回的带颜色的数据进行转换
#npm install ansi_up
class RabbitmqLogger(object):
    def __init__(self,logger,producer=None,exchangeName=None,routeKey=None,logFormat="[%(levelname)s] [%(asctime)s] : %(message)s"
):
        self.__logger =logger
        self.level=self.__logger.level    #logging会用这个，add以后
        self.__producer = producer
        self.__exchangeName=exchangeName
        self.__routeKey=routeKey
        if logFormat is None:self.__formatter = logging.Formatter(LoggerFactory.LOG_FORMAT)
        else:self.__formatter = logging.Formatter(logFormat)

    def handle(self,record):#logging会用这个，add以后
        logRequest = {"requestTime":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"type":record.levelname,"msg":self.__formatter.format(record)}
        try:
            self.__producer.produceMessage(self.__exchangeName,json.dumps(logRequest),self.__routeKey)
        except Exception as e:
            self.__logger.exception(e)          
            self.__logger.error(exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,
             stacklevel=1):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.__logger.findCaller(stack_info, stacklevel)
            except ValueError: # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.__logger.makeRecord(self.__logger.name, level, fn, lno, msg, args,
                                 exc_info, func, extra, sinfo)
        self.handle(record)     
    def setLevel(self, level):
        self.__logger.setLevel(level)
        self.level=self.__logger.level
    def isEnabledFor(self, level):
        return True# or return self.__logger.isEnabledFor(level)
    def debug(self,msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)        
    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kwargs)    
    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, args, **kwargs)  
    def warn(self, msg, *args, **kwargs):
        self.__logger.warn(msg, *args, **kwargs)
        if self.isEnabledFor(WARN):
            self._log(WARN, msg, args, **kwargs)        
    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)        
    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.__logger.exception(msg, *args,exc_info, **kwargs)
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)
    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, msg, args, **kwargs)        
    def log(self, level, msg, *args, **kwargs):
        self.__logger.log(level,msg, *args, **kwargs)
        if not isinstance(level, int):
            raise TypeError("level must be an integer")
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)               
    def setRabbitmq(self,producer,exchangeName,routeKey):
        self.__producer = producer
        self.__exchangeName=exchangeName
        self.__routeKey=routeKey
     