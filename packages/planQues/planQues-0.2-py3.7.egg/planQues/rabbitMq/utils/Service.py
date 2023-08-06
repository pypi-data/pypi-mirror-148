import pika
#from ai.utils.string_utils import exceptionNow2String
#from ai.settings import stat_logger as logger
# from ai.utils.spawn_utils import spawnAfter
#from planQues.rabbitMq.utils.service_utils import MAX_MESSAGE_PROCESS_SECONDS,PORT,HOST,USER,PASSWORD,VIRTUALHOST
MAX_MESSAGE_PROCESS_SECONDS = 60*60*24*7
PORT = 30672
USER = 'ai'
HOST = '192.168.75.13'
PASSWORD = 'MTExMTEx'
VIRTUALHOST = 'async'

class Service(object):
    def __init__(self,username=USER,password=PASSWORD,serverip=HOST,port=PORT,virtualhost=VIRTUALHOST,heartbeat=10,title="Service",blockedConnectionTimeoutSeconds=MAX_MESSAGE_PROCESS_SECONDS):#最长7天
        self.username =username
        self.password = password
        self.serverip = serverip
        self.port = port
        self.virtualhost = virtualhost
        self.channel=None
        self.heartbeat=heartbeat
        self.connection=None
        self.__title=title+":"
        interval = self.heartbeat
        if interval >4:interval=interval-1
        if interval >4:interval=interval-4
        self.interval=interval
        self.blockedConnectionTimeoutSeconds=blockedConnectionTimeoutSeconds
    def getTitle(self):
        return self.__title
    def setTitle(self,title):
        #logger.info(self.__title+"changeTitle->"+title+":")
        self.__title=title+":"
    #无法在多线程中使用spawn协程，看上去只用最后一个spawn有用。之前的线程里的spawn都会失效，hub放外面也没有用        
#     def __monitorHeartBeatsSpawn(self):#对Python协程的理解 https://blog.csdn.net/ohenry88/article/details/73196798
#         connection=self.connection
#         if connection is None or connection.is_closed:return
#         """Function to send heartbeat checks to RabbitMQ. This keeps the
#            connection alive over long-running processes."""
# 
# #         cref = weakref.ref(connection)
#         logger.info(self.__title+"Starting heartbeat monitor.")
# #     
# #         def heartbeat_check():
# #             conn = cref()
# #             if conn is not None and conn.is_open:
# #                 conn.process_data_events()
# #                 logger.info(self.__title+"Ran heartbeat check.")
# #                 spawn_after(interval, heartbeat_check)
#         return spawnAfter(self.interval, self.__heartbeat_check)
     
#     def __heartbeat_check(self):
#         conn=self.connection
# #         cref = weakref.ref(connection)
# #         conn = cref()
#         if conn is not None and conn.is_open:
#             conn.process_data_events()
#             logger.info(self.__title+"比u一个心跳，Ran heartbeat check.")
#             spawnAfter(self.interval, self.__heartbeat_check)      
#         else:logger.info(self.__title+"Closed, stop heartbeat.")
    def connect(self):
        user_pwd = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host= self.serverip,port=self.port, credentials=user_pwd,virtual_host=self.virtualhost,heartbeat=self.heartbeat,blocked_connection_timeout=self.blockedConnectionTimeoutSeconds))#None))#=0))  # 创建连接
        self.channel = self.connection.channel()
        #logger.info(self.__title+"connect")
    def close(self):
        if self.channel is not None and (not self.channel.is_closed): 
            #取消消费者并返回任何待处理消息
            requeued_messages = self.channel.cancel()
            #logger.info(self.__title+ ('Cancel Requeued %i messages' % requeued_messages))
        if self.connection is not None and self.connection.is_open:
            self.connection.close()
            #logger.info(self.__title+ 'Connection Closed')
    def _checkConnect(self):
        if self.channel is None or self.channel.is_closed:self.connect()
#     def expense(self,queuename,func):
#         """线程不安全，废弃
#         :param queuename: 消息队列名称
#         :param func: 要回调的方法名
#         """
#         def parse_result_func(ch, method, properties, body):
#             try:
#                 ch.connection.add_callback_threadsafe(functools.partial(func, ch, method,properties,body))
#             except Exception as e:
#                 logger.exception(e)          
#                 logger.error(exceptionNow2String())#异常，无法离开imageLeaveBuilding(image.f_id)，离开可能再进入还是错，所以要封锁排查
#                 raise e                
#             finally:
#                 gc.collect()    
#         self._checkConnect()
#         self.channel.basic_qos(prefetch_count=1)
#         self.channel.basic_consume(on_message_callback=parse_result_func,
#                               queue=queuename,
#                               )
#         self.channel.start_consuming()


# def callback(ch, method, properties, body):
#     stat_logger.info(" [消费者] Received %r" % body)
#     time.sleep(1)
#     stat_logger.info(" [消费者] Done")
#     ch.basic_ack(delivery_tag=method.delivery_tag)#  接收到消息后会给rabbitmq发送一个确认
    
# if __name__ != '__main__':
#     try:       
#         Consumer = RabbitmqService(USER,PASSWORD,HOST,PORT,VIRTUALHOST,title="Consumer")
#         Producer = RabbitmqService(USER,PASSWORD,HOST,PORT,VIRTUALHOST,title="Producer")#,needHeartBeat=True)
#     except Exception as err:
#         stat_logger.exception(err)
#         stat_logger.error("get Rabbitmq error: %s" %(str(err)))
# 
# if __name__ == '__main__':
#     import json
#     Consumer = RabbitmqService(USER,PASSWORD,HOST,PORT,VIRTUALHOST)
#     Consumer.connect()
#     data = {"code":3}
#     Consumer.testProductMessage("test3",json.dumps(data))
#     Consumer.expense("test3",callback)
