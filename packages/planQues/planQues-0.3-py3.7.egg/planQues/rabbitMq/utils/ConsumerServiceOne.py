from ai.settings import stat_logger
from ai.utils.string_utils import exceptionNow2String
from ai.settings import stat_logger as logger
# from ai.utils.spawn_utils import spawnAfter
import functools,gc
from ai.planQues.rabbitMq.utils.HeartBeatService import HeartBeatService
from ai.planQues.rabbitMq.utils.service_utils import MAX_MESSAGE_PROCESS_SECONDS,PORT,HOST,USER,PASSWORD,VIRTUALHOST

#one connection one channel one thread

class ConsumerServiceOne(HeartBeatService):
    def __init__(self,username=USER,password=PASSWORD,serverip=HOST,port=PORT,virtualhost=VIRTUALHOST,heartbeat=10,title="ConsumerServiceOne",blockedConnectionTimeoutSeconds=MAX_MESSAGE_PROCESS_SECONDS,needHeartBeat=False,prefetchCount=2):#最长7天
        super(ConsumerServiceOne,self).__init__(username,password,serverip,port,virtualhost,heartbeat,title,blockedConnectionTimeoutSeconds)
        self.prefetchCount=prefetchCount
        self.needHeartBeat=needHeartBeat
    def preConsume(self):
        self._checkConnect()        
    def expense(self,queuename,func):
        """
        :param queuename: 消息队列名称
        :param func: 要回调的方法名
        """
        def parse_result_func(ch, method, properties, body):
            try:
                ch.connection.add_callback_threadsafe(functools.partial(func, ch, method,properties,body))
            except Exception as e:
                logger.exception(e)          
                logger.error(exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
                raise e                
            finally:
                gc.collect()    
        self._checkConnect()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_message_callback=parse_result_func,
                              queue=queuename,
                              )
        self.channel.start_consuming()

    
if __name__ != '__main__':
    try:       
        Consumer = ConsumerServiceOne(USER,PASSWORD,HOST,PORT,VIRTUALHOST,title="Consumer")
    except Exception as err:
        stat_logger.exception(err)
        stat_logger.error("get Rabbitmq error: %s" %(str(err)))

