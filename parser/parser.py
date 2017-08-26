#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: parser.py
@time: 17/8/26 17:16
@desc:
'''
import pickle

class Parser(object):

    def handle_task(self, task):
        response = pickle.loads(task["response_obj"])
        request = pickle.loads(task["request_obj"])
        exec ("from spiders.%s import Spider" % task["spider"])
        exec ("result = Spider().%s(response)" % request.parser)
        if result:
            task["status"] = 3  # success
        else:
            task["status"] = 4  # fail
        task["result"] = result
        return task




