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
    ROOT_URL = 'https://qiita.com/api/v1{0}'
    requests = None

    def __init__(self, **kwargs):
        options = ['url_name', 'password', 'token']
        for option in options:
            if option in kwargs:
                setattr(self, option, kwargs[option])
            else:
                setattr(self, option, None)

        if self.requests is None:
            # TODO: Use urllib?
            self.requests = requests

        if self.token is None and self.url_name and self.password:
            self.login()

    def rate_limit(self):
        """Get api rate limit.

        Max 150 count/hour.
        """
        return self._request('get', '/rate_limit')

    def login(self):
        """login

        Login to Qiita to get token.
        """
        params = {'url_name': self.url_name, 'password': self.password}
        response = self._request('post', '/auth', params)
        if 'token' in response:
            self.token = response['token']

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
        if self.token is not None:
            if params is None:
                params = {}
            params['token'] = self.token

        uri = self.ROOT_URL.format(path)

        response = None
        headers = {'Content-Type': 'application/json'}
        if method == 'get':
            response = self.requests.get(uri, params=params, headers=headers)

        elif method == 'delete':
            response = self.requests.delete(uri, params=params,
                                            headers=headers)
        elif method == 'post':
            response = self.requests.post(uri, data=json.dumps(params),
                                          headers=headers)

        elif method == 'put':
            response = self.requests.put(uri, data=json.dumps(params),
                                         headers=headers)

        if response.ok is False:
            on_complte(response.status_code)

        result = '' if response.content == '' else json.loads(response.content)

        return result
