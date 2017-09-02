#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: __init__.py.py
@time: 17/8/30 10:38
@desc:
'''

import importlib

from frame.core.fetcher import Fetcher
from frame.core.parser import Parser
from frame.http.request import Request

from settings import SPIDERS


class Schedule(object):

    tag = True

    def __init__(
            self,
            inqueue,
            requestqueue,
            parsequeue,
            taskdb,
            taskmanager
    ):
        # storage task one from program and insert into taskdb
        self.inqueue = inqueue
        # storage task one get out from taskdb
        self.requestqueue = requestqueue

        self.parsequeue = parsequeue

        self.taskdb = taskdb
        self.taskmanager = taskmanager

    def get_fetcher(self):
        return Fetcher(self.inqueue, self.taskmanager)

    def get_parser(self):
        return Parser(self.inqueue, self.taskmanager)

    # 启动初始任务
    def start_requests(self, flag):
        for spider_name in SPIDERS:
            spider = importlib.import_module("spiders.%s"%spider_name)
            for request in spider.Spider().start_requests():
                if isinstance(request, Request):
                    task = self.taskmanager.gen_new_task(flag, spider_name, request)
                    self.inqueue.put(task)

    # 管理任务输入
    def insert_or_update_task(self):
        while self.tag:
            task = self.inqueue.get()
            if task.get("status"):
                print("update a task")
                self.taskdb.update(task)
            else:
                print('insert a task')
                self.taskdb.insert(task)

    # 管理任务输出
    def load_request_task_from_db(self, status, flag=None):
        print("request",status)
        while self.tag:
            for spider in SPIDERS:
                for task in self.taskdb.load_tasks_to_queue(status, spider, flag):
                    self.requestqueue.put(task)

    def load_parse_task_from_db(self, status, flag=None):
        print("parse", status)
        while self.tag:
            for spider in SPIDERS:
                for task in self.taskdb.load_tasks_to_queue(status, spider, flag):
                    self.parsequeue.put(task)

    def launch_worker(self, taskqueue, worker, Pool, pool_max):
        pool = Pool(10)
        while self.tag:
            if not taskqueue.empty():
                pool.apply_async(worker.run, args=(taskqueue,))

    @classmethod
    def quit(cls):
        cls.tag = False

# # 调度器控制
# def run_schedule(flag):
#     # 启动初始任务线程
#     # t_start = run_in_thread(start_requests, flag)
#     # 启动任务输入线程
#     t_add_task = run_in_thread(add_task_to_db)
#     # 启动任务输出线程
#     for spider_name in SPIDERS:
#         for status in [1,2]:
#             t_load_task = run_in_thread(load_task_from_db, status, spider_name, flag)
#     t_dispatch = run_in_thread(dispatch)
#     # t_start.join()
#     t_add_task.join()
#     t_dispatch.join()

