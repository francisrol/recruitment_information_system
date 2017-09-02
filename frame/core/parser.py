#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: parser.py
@time: 17/8/28 17:35
@desc:
'''

class Parser(object):
    '''parse Response Object'''

    name = "parser"
    status = 2

    def __init__(self, inqueue, taskmanager):
        self.inqueue = inqueue
        #self.parsequeue = parsequeue
        self.taskmanager = taskmanager

    def handle_result(self, task, result):
        for t in self.taskmanager.handle_result(task, result, self.name):
            self.inqueue.put(t)

    def run(self, taskqueue):
        print("run one parser")
        task = taskqueue.get()

        try:
            response = self.taskmanager.get_response_obj(task)
            parse = self.taskmanager.get_parse_func(task)
            result = parse(response)
        except Exception as e:
            print(e)
            taskqueue.put(task)
        else:
            try:
                self.handle_result(task, result)
            except Exception as e:
                print(e)







