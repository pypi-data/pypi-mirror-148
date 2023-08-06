from ai.settings import stat_logger,RABBITMQ_SERVICE_NAME
from ai.common.conf_utils import get_base_config 
from ai.utils.string_utils import exceptionNow2String
# from ai.utils.spawn_utils import spawnAfter

MAX_MESSAGE_PROCESS_SECONDS=60*60*24*7#最长7天

try:
    G=get_base_config(RABBITMQ_SERVICE_NAME, {})
    PORT = G.get("port") 
    HOST = G.get("host") 
    USER = G.get("user") 
    PASSWORD = str(G.get("passwd"))
    VIRTUALHOST = G.get("virtualhost")
except Exception as e:
    stat_logger.exception(e)     
    stat_logger.error(exceptionNow2String())    


