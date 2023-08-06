from datetime import timedelta,datetime
from ..utils.ProducerService import Producer
from ..exchanges import AI中台交换机
import json
import uuid
import time
import os

#serviceName = os.environ('serviceName')
fm = "%Y-%m-%dT%H:%M:%S.%f"



def mirgeFromHeaders(mResult,headers,keyMaps):
    for key1 in keyMaps:
        if key1 in headers:mResult[keyMaps[key1]]=headers[key1]

def sendLog(request,serviceName,response,headers):
    finalRequest = {}
    finalRequest['data'] = request.copy()
    mirgeFromHeaders(finalRequest, headers, {'X-Request-Id': 'sessionId'})
    finalRequest['time'] = (datetime.fromtimestamp(time.time())+ timedelta(hours=8)).strftime(fm)
    finalRequest['serviceName'] = os.environ.get('serviceName')
    finalRequest['type'] = 1
    finalRequest['uuid'] = str(uuid.uuid4())
    finalRequest['uuid'] = finalRequest['serviceName'] + '_' + finalRequest['uuid']

    finalResponse = {}
    finalResponse['result'] = response
    mirgeFromHeaders(finalResponse,headers,{'X-Request-Id': 'sessionId'})
    finalResponse['time'] = (datetime.fromtimestamp(time.time()) + timedelta(hours=8)).strftime(fm)
    finalResponse['serviceName'] = os.environ.get('serviceName')
    finalResponse['type'] = 2
    finalResponse['uuid'] = str(uuid.uuid4())
    finalResponse['uuid'] = finalResponse['serviceName'] + '_' + finalResponse['uuid']

    Producer.produceMessage(AI中台交换机.应用日志.value, json.dumps(finalRequest))
    Producer.produceMessage(AI中台交换机.应用日志.value, json.dumps(finalResponse))
