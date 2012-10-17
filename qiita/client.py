# -*- coding: utf-8 -*-
"""
    qiita.client
    ~~~~~~~~~~~~

    Python wrapper for Qiita API v1.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import re
import requests
from . import json
from .exceptions import on_complte


class Client(object):
    ROOT_URL = 'https://qiita.com/api/v1{0}'
    options = {'url_name': '', 'password': '', 'token': None}
    requests = None

    def __init__(self, options=None):
        # TODO: Use urllib?
        self.requests = requests
        if options is None:
            return
        for k in self.options:
            if k in options:
                self.options[k] = options[k]

    def rate_limit(self):
        """Get api rate limit.

        Max 150 count/hour.
        """
        return self._request('get', '/rate_limit')

    def login(self):
        """login

        Login to Qiita to get token.
        """
        params = {
            'url_name': self.options['url_name'],
            'password': self.options['password']
        }
        response = self._request('post', '/auth', params)
        if 'token' in response:
            self.options['token'] = response['token']

        return response

    def get(self, path, params=None):
        """GET request.

        :param path:
        :param params:
        """
        return self._request('get', path, params)

    def delete(self, path, params=None):
        """DELETE request.

        :param path:
        :param params:
        """
        return self._request('delete', path, params)

    def post(self, path, params=None):
        """POST request.

        :param path:
        :param params:
        """
        return self._request('post', path, params)

    def put(self, path, params=None):
        """PUT request.

        :param path:
        :param params:
        """
        return self._request('put', path, params)

    def _request(self, method, path, params=None):
        """_requests.

        _requests depends on _requests library.

        see `<http://docs.python-_requests.org/en/latest/>_` more details.

        :param method:
        :param path:
        :param params:
        """
        if self.options['token'] is not None:
            if params is None:
                params = {}
            params['token'] = self.options['token']

        path = self.ROOT_URL.format(path)

        response = None
        headers = {'Content-Type': 'application/json'}
        if method == 'get':
            response = self.requests.get(path, params=params, headers=headers)

        elif method == 'delete':
            response = self.requests.delete(path, params=params,
                                            headers=headers)
        elif method == 'post':
            response = self.requests.post(path, data=json.dumps(params),
                                          headers=headers)

        elif method == 'put':
            response = self.requests.put(path, data=json.dumps(params),
                                         headers=headers)

        if response.error is not None:
            on_complte(response.status_code)

        result = '' if response.content == '' else json.loads(response.content)

        return result
