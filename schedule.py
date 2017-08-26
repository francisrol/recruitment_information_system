#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: schedule.py
@time: 17/8/26 11:28
@desc:
'''
import pickle
from download.fetcher import Fetcher
from init.settings import SPIDERS
from database.redis.taskdb import TaskDB
from http.request import Request
from parser.parser import Parser

class Schedule(object):
    def __init__(self):
        self.taskdb = TaskDB(db=6)
        self.fetcher = Fetcher()
        self.parser = Parser()

    def gen_task(self):
        for spider_name in SPIDERS:
            exec ("from spiders import %s as spider" % spider_name)
            for request in spider.Spider().start_requests():
                if isinstance(request, Request):
                    self.taskdb.insert("index", spider_name, request)

    def launch_fetcher(self, status=1, flag=None):
        for spider_name in SPIDERS:
            for task in self.taskdb.load_tasks(status, spider_name, flag):
                new_task = self.fetcher.handle_task(task)
                print(task["taskid"])
                self.taskdb.update(flag, spider_name, new_task)

    def launch_parser(self, status=2, flag=None):
        for spider_name in SPIDERS:
            for task in self.taskdb.load_tasks(status, spider_name, flag):
                new_task = self.parser.handle_task(task)
                self.taskdb.update(flag, spider_name, new_task)

    def drop_all_tasks(self, flag):
        self.taskdb.drop(flag)

    def load_task(self, status, spider, flag=None):
        return self.taskdb.load_tasks(status, spider, flag=None)

if __name__ == '__main__':
    schedule = Schedule()
    schedule.launch_fetcher(flag="index")
