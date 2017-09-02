#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: run_with_thread.py
@time: 17/9/1 17:56
@desc:
'''

from . import Schedule
from frame.core.queue_manager import QueueManager
from frame.database.redis.taskdb import TaskDB
from frame.core.task_manager import TaskManager
from frame.libs.utils import run_in_thread, get_thread_pool


class RunByThread(object):

    def __init__(self):
        queuemanager = QueueManager()
        self.inqueue = queuemanager.inqueue
        self.requestqueue = queuemanager.requestqueue
        self.parsequeue = queuemanager.parsequeue
        self.taskdb = TaskDB()
        self.taskmanager = TaskManager()

    def get_schedule_object(self):
        return Schedule(
            self.inqueue,
            self.requestqueue,
            self.parsequeue,
            self.taskdb,
            self.taskmanager
        )

    def start(self, flag):
        from six.moves import input
        schedule = self.get_schedule_object()
        parser = schedule.get_parser()
        fetcher = schedule.get_fetcher()
        print("爬虫资讯系统V1.0")
        print("1. 创建初始任务")
        print("2. 启动下载器")
        print("3. 启动解析器")
        print("4. 启动任务输入队列")
        print("5. 启动任务输出队列")
        print("6. 退出\n")

        threads = []
        while True:
            cmd = input("请输入cmd: ")
            if cmd == '1':
                schedule.start_requests(flag)
                print("初始任务创建成功")
            if cmd == '2':
                fetcher_manage_thread = run_in_thread(schedule.launch_worker, self.requestqueue, fetcher,get_thread_pool, 15)
                threads.append(fetcher_manage_thread)
                print("抓取器管理线程启动成功")
            if cmd == '3':
                parser_manage_thread = run_in_thread(schedule.launch_worker, self.parsequeue, parser,get_thread_pool, 15)
                threads.append(parser_manage_thread)
                print("解析器管理线程启动成功")
            if cmd == '4':
                taskin_thread = run_in_thread(schedule.insert_or_update_task)
                threads.append(taskin_thread)
                print("任务输入队列管理线程启动成功")
            if cmd == '5':
                fetcher_task_thread = run_in_thread(
                    schedule.load_request_task_from_db,
                    fetcher.status,
                    flag
                )
                parser_task_thread = run_in_thread(
                    schedule.load_parse_task_from_db,
                    parser.status,
                    flag
                )
                threads.append(fetcher_task_thread)
                threads.append(parser_task_thread)
                print("任务输出队列管理线程启动成功")
            if cmd == '6':
                schedule.quit()
                for t in threads:
                    t.join()
                import sys
                sys.exit(0)





