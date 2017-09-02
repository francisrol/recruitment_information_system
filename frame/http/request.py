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

from .response import Response

class Request(object):
    def __init__(self, url, parse, method="GET", validate=None,
                params=None, data=None, headers=None, cookies=None,
                timeout=None, allow_redirects=True, json=None, meta=None):
        self._method = method
        self._url = url
        self._parse = parse
        self._validate = validate
        self._params = params
        self._data = data
        self._headers = headers
        self._cookies = cookies
        self._timeout = timeout
        self._allow_redirects = allow_redirects
        self._json = json
        self._meta = meta

    def fetch(self):
        try:
            response = Session().request(
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
            response.meta = self._meta
        except Exception as e:
            return e
        else:
            return response

    @property
    def parse(self):
        return self._parse

    @property
    def validate(self):
        return self._validate

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._url

