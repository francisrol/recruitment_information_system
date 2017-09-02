#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: queue_manager.py
@time: 17/8/28 17:35
@desc:
'''
from frame.database.redis.taskdb import TaskDB
from frame.task_queue.redis_queue import Queue

class QueueManager(object):

    def __init__(self):
        self.__inqueue = Queue("inqueue", maxsize=1800)
        self.__requestqueue = Queue("requestqueue", maxsize=1800)
        self.__parsequeue = Queue("parsequeue", maxsize=1800)

    @property
    def inqueue(self):
        return self.__inqueue

    @property
    def parsequeue(self):
        return self.__parsequeue

    @property
    def requestqueue(self):
        return self.__requestqueue




