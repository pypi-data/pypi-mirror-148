import pika
#from ai.utils.string_utils import exceptionNow2String
#from ai.settings import stat_logger as logger
# from ai.utils.spawn_utils import spawnAfter
#from planQues.rabbitMq.utils.service_utils import MAX_MESSAGE_PROCESS_SECONDS,PORT,HOST,USER,PASSWORD,VIRTUALHOST
from .HeartBeatService import HeartBeatService
MAX_MESSAGE_PROCESS_SECONDS = 60*60*24*7
PORT = 30672
USER = 'ai'
HOST = '192.168.75.13'
PASSWORD = 'MTExMTEx'
VIRTUALHOST = 'async'

class ProducerService(HeartBeatService):
    def __init__(self,username=USER,password=PASSWORD,serverip=HOST,port=PORT,virtualhost=VIRTUALHOST,heartbeat=10,title="ProducerService",blockedConnectionTimeoutSeconds=MAX_MESSAGE_PROCESS_SECONDS,needHeartBeat=True):#最长7天
        super(ProducerService,self).__init__(username,password,serverip,port,virtualhost,heartbeat,title,blockedConnectionTimeoutSeconds,needHeartBeat)
    def produceMessage(self,exchangeName,message,routeKey='noKey',deliveryMode=2):
        if not self.__produceMessage(exchangeName, message, routeKey, deliveryMode):
            self.close()
            self.connect()
            self.__produceMessage(exchangeName, message, routeKey, deliveryMode,False)
    def __produceMessage(self,exchangeName,message,routeKey='noKey',deliveryMode=2,hideExeption=True):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            self._checkConnect()
            self.channel.basic_publish(exchange=exchangeName,routing_key=routeKey,body=message,    #要发送的消息
                                  properties=pika.BasicProperties(delivery_mode=deliveryMode)#设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                                  )
            return True
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())#异常
                raise e
        finally:
            self._lock.release()#解锁，离开该资源
        return False
    def newQue(self,queueName,exchangeName,routeKey='no', durableType=True):
        if not self.__newQue(queueName,exchangeName,routeKey, durableType,True):
            self.close()
            self.connect()
            self.__newQue(queueName,exchangeName,routeKey, durableType)
    def __newQue(self,queueName,exchangeName,routeKey='no', durableType=True,hideExeption=False):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            self._checkConnect()
            #logger.debug("newQue.queue_declare={}".format(queueName))
            self.channel.queue_declare(queue=queueName, durable=durableType)
            #logger.debug("newQue.queue_bind={}".format(queueName))
            self.channel.queue_bind(queue=queueName,exchange=exchangeName,routing_key=routeKey)
            return True
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
                raise e
        finally:
            self._lock.release()#解锁，离开该资源
        return False
    def deleteQue(self,queueName,exchangeName):
        if not self.__deleteQue(queueName,exchangeName,True):
            self.close()
            self.connect()
            self.__deleteQue(queueName,exchangeName)
    def __deleteQue(self,queueName,exchangeName,hideExeption=False):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            self._checkConnect()
            self.channel.queue_unbind(queueName,exchange=exchangeName)
            self.channel.queue_delete(queueName)
            return True
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
                raise e
        finally:
            self._lock.release()#解锁，离开该资源
        return False
    def unbindQue(self,queueName,exchangeName,routeKey=None):
        if not self.__unbindQue(queueName,exchangeName,routeKey,True):
            self.close()
            self.connect()
            self.__unbindQue(queueName,exchangeName,routeKey)
    def __unbindQue(self,queueName,exchangeName,routeKey=None,hideExeption=False):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            self._checkConnect()
            self.channel.queue_unbind(queueName,exchange=exchangeName,routing_key=routeKey)
            return True
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
                raise e
        finally:
            self._lock.release()#解锁，离开该资源
        return False
    def newExchange(self,exchangeName,exchangeType='fanout',passive=False,durable=True):
        if not self.__newExchange(exchangeName,exchangeType,passive,durable,True):
            self.close()
            self.connect()
            self.__newExchange(exchangeName,exchangeType,passive,durable)
    def __newExchange(self,exchangeName,exchangeType='fanout',passive=False,durable=True,hideExeption=False):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            self._checkConnect()
            self.channel.exchange_declare(exchangeName,exchangeType,passive,durable)
            return True
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
                raise e
        finally:
            self._lock.release()#解锁，离开该资源
        return False
#     def testProductMessage(self,queuename,message):
#         self._checkConnect()
#         self.channel.queue_declare(queue=queuename, durable=True)
#         self.channel.basic_publish(exchange='',
#                               routing_key=queuename,#写明将消息发送给队列queuename
#                               body=message,    #要发送的消息
#                               properties=pika.BasicProperties(delivery_mode=2,)#设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
#                               )

if __name__ != '__main__':
    Producer = ProducerService(USER,PASSWORD,HOST,PORT,VIRTUALHOST,title="Producer")