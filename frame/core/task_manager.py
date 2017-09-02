#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: task_manager.py
@time: 17/8/28 17:48
@desc:
'''

__task__ = {
    "taskid": str,
    "flag": str,
    "spider": str,
    "status": int,
    "schedule": {
        "retries": int,
        "retried": int,
    },
    "request": {
        "object": str, # pickle
        "method": str,
        "parse": str, #
        "validate": str,
    },
    "response": {
        "object": str, # pickle
        "status_code": int,
    },
    "parseresult": {
        "data": str,
    },
    "updatetime": int,
}

import types
import pickle
import time
import hashlib
import importlib

from . import fetcher, parser
from frame.http.request import Request
from frame.http.response import Response

class Task(dict):

    def __init__(self, flag, spider, request, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.flag = flag
        self.spider = spider
        self._request = request

    def _gen_taskid(self):
        '''use sha1 to gen a taskid by some fields'''
        #print(isinstance(self._request, Request))
        assert isinstance(self._request, Request), "Invalid request object"
        sorted_params = sorted([str(temp) for temp in self._request._params.iter()]) if self._request._params else None
        sorted_data = sorted([str(temp) for temp in self._request._data.iter()]) if self._request._data else None
        sha1 = hashlib.sha1()
        sha1.update(self._request._url)
        sha1.update(self._request._method)
        sha1.update(sorted_params or b"")
        sha1.update(sorted_data or b"")
        return sha1.hexdigest()

    @property
    def taskid(self):
        '''gen and return taskid'''
        return self._gen_taskid()


class TaskManager(object):
    '''manage task(dict) object'''

    def gen_new_task(self, flag, spider, request):
        '''
        gen a task from flag, spider_name, request without status
        '''
        task = Task(flag, spider, request)
        task["taskid"] = task.taskid
        task["flag"] = flag
        task["spider"] = spider

        request_ = {}
        request_["object"] = pickle.dumps(request)
        request_["method"] = request.method
        request_["url"] = request.url
        request_["parse"] = request.parse
        request_["validate"] = request.validate

        task["request"] = request_
        task["updatetime"] = time.time()
        return task

    def get_request_obj(self, task):
        '''return request object from task'''
        request = task.get("request").get("object")
        assert request, "Invalid request object"
        return pickle.loads(request)

    def get_response_obj(self, task):
        '''return response object from task'''
        response = task.get("response").get("object")
        assert response, "Invalid Response Object"
        response = pickle.loads(response)
        assert isinstance(response, Response), "Invalid Response Object"
        return response

    def get_parse_func(self, task):
        '''return spider's parse method from task'''
        spider = importlib.import_module("spiders.%s" % task["spider"])
        parse = getattr(spider.Spider(), task["request"]["parse"])
        return parse

    def get_validate_func(self, task):
        '''return spider's validate method from task'''
        if not task["request"]["validate"]:
            return lambda temp:True
        spider = importlib.import_module("spiders.%s" % task["spider"])
        validate = getattr(spider.Spider(), task["request"]["validate"])
        return validate

    def update_task(self, task, **kwargs):
        '''update task'''
        task.update(kwargs)

    def handle_result(self, task, result, comefrom):
        '''handle result by comefrom'''
        if comefrom == parser.Parser.name:
            return self.handle_parser_result(task, result)
        elif comefrom == fetcher.Fetcher.name:
            return self.handle_fetcher_result(task, result)
        else:
            assert 0, "Cannot handle result come from %s"%comefrom

    def handle_fetcher_result(self, task, result):
        '''handle fetcher's result and return a updated task'''
        if isinstance(result, Response):
            response = {}
            response["object"] = pickle.dumps(result)
            response["status_code"] = result.status_code
            self.update_task(task, response=response, status=2)
            return task
        else:
            self.update_task(task, status=4, error_message=str(result))
            return task

    def handle_parser_result(self, task, result):
        '''handle parser's result and return a updated task or a new task'''
        def handle(res):
            if isinstance(res, Request):
                new_task = self.gen_new_task(task["flag"], task["spider"], res)
                return new_task
            else:
                validate = self.get_validate_func(task)
                flag = validate(res)
                status = 3 if flag else 4
                parseresult = {}
                parseresult["data"] = res
                self.update_task(task, parseresult=parseresult, status=status)
                return task

        if isinstance(result, types.GeneratorType):
            for r in result:
                yield handle(r)
        else:
            yield handle(result)






