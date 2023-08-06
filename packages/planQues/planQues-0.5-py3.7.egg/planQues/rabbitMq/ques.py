# -*- coding: utf-8 -*-
# import os,sys
# env='prod'
# if len(sys.argv)>1:env=sys.argv[1]
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings.'+env)

from enum import Enum,unique
@unique
class AI中台交换机(Enum):
    镜像构建='aiPlatform/image/buildRequest'

@unique
class 镜像构建队列(Enum):
    构建请求='imageBuildRequest'

@unique
class 应用日志队列(Enum):
    日志事件='logEvent'
    模型数据='modleData'
    
@unique
class 模型构建队列(Enum):
    构建请求='modelBuildRequest'
    
@unique
class 模型部署队列(Enum):
    构建请求='modelK8sdeployRequest'