#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: taskdb.py
@time: 17/8/24 20:29
@desc:
'''

import itertools
import json
import logging
import time
import six
import pickle
import redis

from database.base.taskdb import TaskDB as BaseTaskDB
from libs import utils


class TaskDB(BaseTaskDB):
    __prefix__ = 'taskdb_'

    def __init__(self, host="127.0.0.1", port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        try:
            self.redis.scan(count=1)
            self.scan_available = True
        except Exception as e:
            logging.debug("redis_scan disabled: %r", e)
            self.scan_available = False

    def _gen_key(self, flag, spider, taskid):
        return "%s%s_%s_%s" % (self.__prefix__, flag, spider, taskid)

    def _gen_status_key(self, flag, spider, status):
        return '%s%s_%s_status_%d' % (self.__prefix__, flag, spider, status)

    def _parse(self, data):
        if six.PY3:
            result = {}
            for key, value in data.items():
                if isinstance(value, bytes):
                    value = utils.text(value)
                result[utils.text(key)] = value
            data = result

        for each in ("schedule", "request", "response", "result"):
            if each in data:
                if data[each]:
                    data[each] = json.loads(data[each])
                else:
                    data[each] = {}
        if 'status' in data:
            data['status'] = int(data['status'])
        if 'lastcrawltime' in data:
            data['lastcrawltime'] = float(data['lastcrawltime'] or 0)
        if 'updatetime' in data:
            data['updatetime'] = float(data['updatetime'] or 0)
        return data

    def _stringify(self, data):
        for each in ("request", "response", "result"):
            if each in data:
                data[each] = json.dumps(data[each])
        return data

    @property
    def flags(self):
        self._flags = set(utils.text(x) for x in self.redis.smembers(self.__prefix__ + 'flags'))
        return self._flags

    def load_tasks(self, status, spider, flag=None, keys=None):
        if flag is None:
            flag = self.flags
        elif not isinstance(flag, list):
            flag = [flag, ]

        if self.scan_available:
            # 如果可以使用scan
            scan_method = self.redis.sscan_iter
        else:
            scan_method = self.redis.smembers

        # 如果只需要其中某段
        if keys:
            def get_method(name):
                obj = self.redis.hmget(name, keys)
                if all(x is None for x in obj):
                    return None
                return dict(zip(keys, obj))
        else:
            get_method = self.redis.hgetall

        for f in flag:   # 依次返回结果
            status_key = self._gen_status_key(f, spider, status)
            for taskid in scan_method(status_key):
                obj = get_method(self._gen_key(f, spider, utils.text(taskid)))
                if not obj:
                    continue
                else:
                    yield self._parse(obj)

    def get_task(self, flag, spider, taskid, fields=None):
        if fields:
            obj = self.redis.hmget(self._gen_key(flag, spider, taskid), fields)
            if all(x is None for x in obj):
                return None
            obj = dict(zip(fields, obj))
        else:
            obj = self.redis.hgetall(self._gen_key(flag, spider, taskid))

        if not obj:
            return None
        return self._parse(obj)

    def status_count(self, flag, spider):
        '''
        return a dict
        '''
        pipe = self.redis.pipeline(transaction=False)
        for status in range(1, 6):
            pipe.scard(self._gen_status_key(flag, spider, status))
        ret = pipe.execute()

        result = {}
        for status, count in enumerate(ret):
            if count > 0:
                result[status + 1] = count
        return result

    def insert(self, flag, spider, obj, task={}):
        '''
        task = {
            "taskid": str,
            "flag": str,
            "spider": str,
            "status": int,
            # "callback": str,    # pickle
            "request_obj": str,    # pickle

            "response_obj": str,
            "updatetime": int,
        }
        '''
        taskid = obj.taskid
        print(taskid)
        task["taskid"] = taskid
        task["flag"] = flag
        task["spider"] = spider
        task["request_obj"] = pickle.dumps(obj)
        task["updatetime"] = time.time()
        task.setdefault("status", self.ACTIVE)

        task_key = self._gen_key(flag, spider, taskid)

        pipe = self.redis.pipeline(transaction=False)
        if flag not in self.flags:
            # 加入标记
            pipe.sadd(self.__prefix__ + "flags", flag)
        # 保存任务对象
        pipe.hmset(task_key, self._stringify(task))
        # 标记任务的状态
        pipe.sadd(self._gen_status_key(flag, spider, task["status"]), taskid)
        pipe.execute()

    def update(self, flag, spider, task, **kwargs):
        task.update(kwargs)
        task['updatetime'] = time.time()

        pipe = self.redis.pipeline(transaction=False)
        pipe.hmset(self._gen_key(flag, spider, task["taskid"]), self._stringify(task))
        if 'status' in task:
            for status in range(1, 6):
                if status == task['status']:
                    pipe.sadd(self._gen_status_key(flag, spider, task["status"]), task["taskid"])
                else:
                    pipe.srem(self._gen_status_key(flag, spider, task["status"]), task["taskid"])
        pipe.execute()

    def drop(self, flag):
        self.redis.srem(self.__prefix__ + 'flags', flag)

        if self.scan_available:
            scan_method = self.redis.scan_iter
        else:
            scan_method = self.redis.keys

        for each in itertools.tee(scan_method("%s%s_*" % (self.__prefix__, flag)), 100):
            each = list(each)
            if each:
                self.redis.delete(*each)



