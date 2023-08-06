from ai.utils.string_utils import exceptionNow2String
from ai.settings import stat_logger as logger
import functools
from multiprocessing.pool import ThreadPool
from multiprocessing import Process
from ai.planQues.rabbitMq.utils.Service import Service
from ai.planQues.rabbitMq.utils.service_utils import MAX_MESSAGE_PROCESS_SECONDS,PORT,HOST,USER,PASSWORD,VIRTUALHOST
 

class ConsumerService(Service):
    def __init__(self,username=USER,password=PASSWORD,serverip=HOST,port=PORT,virtualhost=VIRTUALHOST,heartbeat=10,title="ConsumerService",blockedConnectionTimeoutSeconds=MAX_MESSAGE_PROCESS_SECONDS,prefetchCount=2):#最长7天
        super(ConsumerService,self).__init__(username,password,serverip,port,virtualhost,heartbeat,title,blockedConnectionTimeoutSeconds)
        self.tp = None
        self.rt = []
        self.prefetchCount=prefetchCount
    def preConsume(self):
        self._checkConnect()        
    def work(self, ch, method, processor,connection,properties,body):
        processor.parse_result_func(ch, method, properties, body)
        cb = functools.partial(ch.basic_ack, delivery_tag=method.delivery_tag)
        connection.add_callback_threadsafe(cb)
        return 1      
    def callback(self, ch, method, properties, body, args):
        processor = args[0]
        connection = args[1]
        rt = self.tp.apply_async(func=self.work, args=(ch, method,processor,connection,properties, body))
        self.rt.append(rt)
        # ch.basic_ack(delivery_tag=method.delivery_tag)  # 非线程安全确认 

    def consumer(self,queuename,processor):
        if self.tp is None:self.tp = ThreadPool(self.prefetchCount)
        self._checkConnect()
        self.channel.basic_qos(prefetch_count=self.prefetchCount)
        # channel.queue_declare(queue='queue', durable=True)
        # 便函数绑定默认的参数 是连接对象 在任务完成时进行消费确认
        callback = functools.partial(self.callback, args=(processor,self.connection,))
        self.channel.basic_consume(
            queue=queuename,  # 队列balance
            on_message_callback=callback,
        )
        self.channel.start_consuming()  # 长时间测试 阻塞
        self.tp.close()
        self.tp.join()
        self.channel.cancel()  # 清除消费者
        self.channel.close()
        self.connection.close()
    def __call__(self):
        p1 = Process(target=self.consumer)
        # p2 = Process(target=self.consumer)
        p1.start()
#         print('p1 start')
        # p2.start()
        # print('p2 start')
        p1.join()
        # p2.join()

if __name__ != '__main__':
    try:       
        Consumer = ConsumerService(USER,PASSWORD,HOST,PORT,VIRTUALHOST,title="Consumer")
    except Exception as err:
        logger.exception(err)
        logger.error(exceptionNow2String())
