from logging import Formatter
class MyFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super(MyFormatter,self).__init__(fmt,datefmt,style,validate)
        self.__sender=None
    def setSender(self,sender):
        self.__sender=sender
    def format(self, record):
        if self.__sender is None:
            return super(MyFormatter,self).format(record)
        formatedStr=super(MyFormatter,self).format(record)
        self.__sender.send(record.levelname,formatedStr)
        return formatedStr
