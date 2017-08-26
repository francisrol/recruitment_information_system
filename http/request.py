#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@license: (C) Copyright 2017
@contact: ryomawithlst@sina.com
@software: PyCharm
@file: request.py
@time: 17/8/26 10:47
@desc:
'''
import hashlib
from requests.sessions import Session

class Request(object):
    def __init__(self, url, parser, method="GET",
                params=None, data=None, headers=None, cookies=None,
                timeout=None, allow_redirects=True, json=None):
        self._method = method
        self._url = url
        self._parser = parser
        self._params = params
        self._data = data
        self._headers = headers
        self._cookies = cookies
        self._timeout = timeout
        self._allow_redirects = allow_redirects
        self._json = json

    def fetch(self):
        return Session().request(
            method=self._method,
            url=self._url,
            params=self._params,
            data=self._data,
            headers=self._headers,
            cookies=self._cookies,
            timeout=self._timeout,
            allow_redirects=self._allow_redirects,
            json=self._json
        )

    def _gen_taskid(self):
        sorted_params = sorted([str(temp) for temp in self._params.iter()]) if self._params else None
        sorted_data = sorted([str(temp) for temp in self._data.iter()]) if self._data else None
        sha1 = hashlib.sha1()
        sha1.update(self._url)
        sha1.update(self._method)
        sha1.update(sorted_params or b"")
        sha1.update(sorted_data or b"")
        return sha1.hexdigest()

    @property
    def taskid(self):
        return self._gen_taskid()

    @property
    def parser(self):
        return self._parser


