# -*- coding: utf-8 -*-
"""
    qiita.client
    ~~~~~~~~~~~~

    Python wrapper for Qiita API v1.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import requests
from . import json
from .exceptions import on_complte


class Client(object):
    ROOT_URL = 'https://qiita.com/api/v1/{0}'
    options = {'url_name': '', 'password': '', 'token': ''}
    requests = None

    def __init__(self, options=None):
        self.requests = requests
        if options is None:
            return
        for k in self.options:
            if k in options:
                self.options[k] = options[k]

    def rate_limit(self):
        return self.request('get', self.ROOT_URL.format('/rate_limit'))

    def login(self):
        pass

    def connection(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def request(self, method, path, params=None):
        if method == 'get':
            response = self.requests.get(path, params=params)
        elif method == 'delete':
            response = self.requests.delete(path, params)
        elif method == 'post':
            response = self.requests.post(path, params)
        elif method == 'put':
            response = self.requests.put(path, params)

        if response.status_code != 200:
            on_complte(response.status_code)

        result = '' if response.content == '' else json.loads(response.content)

        return result
