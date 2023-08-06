# -*- coding: utf-8 -*-
# import os,sys
# env='prod'
# if len(sys.argv)>1:env=sys.argv[1]
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings.'+env)

from enum import Enum,unique
@unique
class AI中台交换机(Enum):
    镜像构建='aiPlatform/image/buildRequest'
    镜像构建日志='aiPlatform/image/buildLog'
    模型构建='aiPlatform/model/buildRequest'
    模型构建日志='aiPlatform/model/buildLog'
    模型部署='aiPlatform/model/k8sdeployRequest'
    模型部署日志='aiPlatform/model/k8sdeployLog'
    应用日志='aiPlatform/app/log'
