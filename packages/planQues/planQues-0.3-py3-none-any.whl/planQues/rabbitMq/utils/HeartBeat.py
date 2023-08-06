#!/usr/bin
#coding: utf-8
#https://blog.csdn.net/moxiaomomo/article/details/77414831
import time
#from ai.settings import stat_logger as logger
import threading
# 
# USER = 'guest'
# PWD = 'guest'
# TEST_QUEUE = 'just4test'

class HeartBeat(threading.Thread):
    def __init__(self, connection,interval,title,service):
        super(HeartBeat, self).__init__()
        self.lock = threading.Lock()
        self.connection = connection
        self.quitflag = False
        self.stopflag = True
        self.setDaemon(True)
        self.interval=interval
        self.__title=title
        self.service=service

    def run(self):
        while not self.quitflag:
            time.sleep(self.interval)
            self.lock.acquire()
            if self.stopflag or self.quitflag :
                self.lock.release()
                continue
            try:
                if self.service.heartBeat():
                    pass#logger.debug(self.__title+"比u一个心跳，Ran heartbeat check.")
                else:
                    #logger.debug(self.__title+"Closed, stop heartbeat.")
                    self.quitflag=True
            except Exception as ex:
                #logger.warn(self.__title+"Error format: %s"%(str(ex)))
                return
            finally:self.lock.release()
    def stopHeartBeat(self):
        self.lock.acquire()
        if self.stopflag==True:
            self.lock.release()
            return
        self.quitflag=True
        #logger.info(self.__title+"Closed, stop heartbeat.")
        self.lock.release()
    def startHeartBeat(self):
        self.lock.acquire()
        if self.quitflag==True:
            self.lock.release()
            return
        self.stopflag=False
        #logger.info(self.__title+"start heartbeat thread.")
        self.lock.release()

# def callback(ch, method, properties, body):
#     logger.info("recv_body:%s" % body)
#     time.sleep(600)
#     ch.basic_ack(delivery_tag = method.delivery_tag)
# 
# def test_main():
#     s_conn = pika.BlockingConnection(
#         pika.ConnectionParameters('127.0.0.1', 
#             heartbeat_interval=10,
#             socket_timeout=5,
#             credentials=pika.PlainCredentials(USER, PWD)))
#     chan = s_conn.channel()
#     chan.queue_declare(queue=TEST_QUEUE)
#     chan.basic_consume(callback,
#                        queue=TEST_QUEUE)
# 
#     heartbeat = HeartBeat(s_conn)
#     heartbeat.start()          #开启心跳线程
#     heartbeat.startHeartBeat()
#     chan.start_consuming()
# 
# if __name__ == "__main__":
#     test_main()