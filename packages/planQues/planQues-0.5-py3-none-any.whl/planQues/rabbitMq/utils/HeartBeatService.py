#from ai.utils.string_utils import exceptionNow2String
#from ai.settings import stat_logger as logger
# from ai.utils.spawn_utils import spawnAfter
from .Service import Service
#from ai.planQues.rabbitMq.utils.service_utils import MAX_MESSAGE_PROCESS_SECONDS,PORT,HOST,USER,PASSWORD,VIRTUALHOST
import threading
from .HeartBeat import HeartBeat
MAX_MESSAGE_PROCESS_SECONDS = 60*60*24*7
PORT = 30672
USER = 'ai'
HOST = '192.168.75.13'
PASSWORD = 'MTExMTEx'
VIRTUALHOST = 'async'

class HeartBeatService(Service):
    def __init__(self,username=USER,password=PASSWORD,serverip=HOST,port=PORT,virtualhost=VIRTUALHOST,heartbeat=10,title="ProducerService",blockedConnectionTimeoutSeconds=MAX_MESSAGE_PROCESS_SECONDS,needHeartBeat=False):#最长7天
        super(HeartBeatService,self).__init__(username,password,serverip,port,virtualhost,heartbeat,title,blockedConnectionTimeoutSeconds)
        self.needHeartBeat=needHeartBeat
        self.heartbeatThread=None
        self._lock = threading.Lock()
    def __monitorHeartBeats(self):
        #logger.info(self.getTitle()+"Starting heartbeat monitor.")
        if self.heartbeatThread is None:
            self.heartbeatThread = HeartBeat(self.connection,self.interval,self.getTitle(),self)
            self.heartbeatThread.start()          #开启心跳线程
        self.heartbeatThread.startHeartBeat()  
    def heartBeat(self,hideExeption=False):
        self._lock.acquire()#加锁，锁住相应的资源
        try:
            if self.connection is not None and self.connection.is_open:    
                self.connection.process_data_events()
                return True
            return False
        except Exception as e:
            if not hideExeption:
                #logger.exception(e)
                #logger.error(self.getTitle()+exceptionNow2String())
                raise e
        finally:        
            self._lock.release()#解锁，离开该资源
    def connect(self):
        super(HeartBeatService,self).connect()
        if self.needHeartBeat:self.__monitorHeartBeats()

    def close(self):
        if self.heartbeatThread is not None:self.heartbeatThread.stopHeartBeat()
        super(HeartBeatService,self).close()           
