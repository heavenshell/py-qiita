# -*- coding: utf-8 -*-
"""
    Add comment here
    ~~~~~~~~~~~~~~~~

    Add descripton here


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client

class Tags(Client):
    def tag_items(self, url_name, params=None):
        params = {} if params is None else params
        return self.get('/tags/${url_name}/items'.format(url_name), params)

    def tags(self, params=None):
        params = {} if params is None else params

        return self.get('/tags/', params)
