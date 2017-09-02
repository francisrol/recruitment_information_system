#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: settings.py
@time: 17/7/25 14:46
@desc:
'''
import os

BASEDIR = os.path.abspath("")

# chromedriver路径
CHROMEDRIVER_PATH = './environments/Chrome/Application/chromedriver'

# 地区列表
CITY = [
    u"北京",
    u"上海",
    u"广州",
    u"深圳",
    u"武汉",
    u"成都",
    u"重庆",
    u"郑州",
    u"杭州",
    u"济南",
    u"南京",
    u"西安",
    u"长沙",
    u"哈尔滨",
    u"石家庄",
    u"合肥",
    u"太原",
]

# 关键词搜索列表
KEYWORDS = [
    "android",
    "c++",
    ".net",
    "java",
    "php",
    "ios",
    u"前端",
    u"游戏开发",
    "python",
    u"产品专员",
    u"产品助理",
    u"产品经理",
    u"运营助理",
    u"运营专员",
    u"运营经理",
    "AR",
    "VR",
    u"大数据",
    u"策划",
    u"新媒体",
    u"推广",
    "sem",
    "seo",
    u"淘宝运营",
    "UE",
    "UI ",
    u"网页设计",
    u"电商设计",
    u"平面设计",
    u"淘宝美工"
]

# 电子商务类型搜索列表
# E_COMMERCES = [
#     u"策划",
#     u"新媒体",
#     u"推广",
#     u"SEM",
#     u"SEO",
#     u"淘宝运营",
# ]

# MongoDB config
MONGOCONFIG = {
    "host":"127.0.0.1",
    "port": 27017
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379
}

SPIDERS = [
    'qc_job',
    #'zl_job'
]
