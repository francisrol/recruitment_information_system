#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: fetcher.py
@time: 17/8/26 15:50
@desc:
'''
import pickle
from http.request import Request

class Fetcher(object):

    def handle_task(self, task):
        request = pickle.loads(task["request_obj"])
        response = request.fetch()
        if response:
            task["status"] = 2  # parse
        else:
            task["status"] = 4  # faile
        task["response_obj"] = pickle.dumps(response)
        return task


