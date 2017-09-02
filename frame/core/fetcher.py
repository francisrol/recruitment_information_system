#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: fetcher.py
@time: 17/8/28 17:35
@desc:
'''
from frame.http.response import Response

class Fetcher(object):
    '''manage Request object and fetch response'''

    name = "fetcher"
    status = 1

    def __init__(self, inqueue, taskmanager):
        #self.requestqueue = requestqueue
        self.inqueue = inqueue
        self.taskmanager = taskmanager

    def fetch(self, request):
        return request.fetch()

    def run(self, taskqueue):
        print("run one fetcher")
        task = taskqueue.get()
        try:
            request = self.taskmanager.get_request_obj(task)
            response = self.fetch(request)
            print(response, response.url)
        except Exception as e:
            print(e)
            taskqueue.put(task)
        else:
            task = self.taskmanager.handle_result(task, response, self.name)
            self.inqueue.put(task)


