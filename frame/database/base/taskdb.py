#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: taskdb2.py
@time: 17/8/24 19:58
@desc:
'''

class TaskDB(object):
    ACTIVE = 1  # 激活
    PARSING = 2  # 待解析
    SUCCESS = 3  # 解析成功
    FAILED = 4  # 解析失败，待重试
    BAD = 5  # 无效请求

    QUEUE = 9 # 正在队列中处理

    flags = set()

    def load_tasks(self, status, spider=None, ):
        raise NotImplementedError

    def get_task(self, project, taskid, fields=None):
        raise NotImplementedError

    def status_count(self, project):
        '''
        return a dict
        '''
        raise NotImplementedError

    def insert(self, project, taskid, obj={}):
        raise NotImplementedError

    def update(self, project, taskid, obj={}, **kwargs):
        raise NotImplementedError

    def drop(self, project):
        raise NotImplementedError

    @staticmethod
    def status_to_string(status):
        return {
            1: 'ACTIVE',
            2: 'SUCCESS',
            3: 'FAILED',
            4: 'BAD',
        }.get(status, 'UNKNOWN')

    @staticmethod
    def status_to_int(status):
        return {
            'ACTIVE': 1,
            'SUCCESS': 2,
            'FAILED': 3,
            'BAD': 4,
        }.get(status, 4)

    def copy(self):
        '''
        database should be able to copy itself to create new connection
        it's implemented automatically by pyspider.database.connect_database
        if you are not create database connection via connect_database method,
        you should implement this
        '''
        raise NotImplementedError




