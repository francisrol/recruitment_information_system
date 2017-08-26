#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: manage.py
@time: 17/8/25 21:30
@desc:
'''
import pickle
from schedule import Schedule
from download.fetcher import Fetcher
from init.settings import SPIDERS

def dispatch():
    schedule = Schedule()
    for spider_name in SPIDERS:
        exec("from spiders import %s as spider"%spider_name)
        for request in spider.Spider().start_requests():
            schedule.dispatch("index", spider_name, request)

def drop_tasks():
    schedule = Schedule()
    schedule.drop_all_tasks("index")

def fetch():
    fetcher = Fetcher()
    schedule = Schedule()
    for spider_name in SPIDERS:
        for task in schedule.load_task(1, spider_name, "index"):
            request = pickle.loads(task["request_obj"])
            response = request.fetch()
            exec("from spiders.%s import Spider"%task["spider"])
            exec("result = Spider().%s(response)"%request.parser)
            print(result)

if __name__ == '__main__':
    # drop_tasks()
    # dispatch()
    fetch()

