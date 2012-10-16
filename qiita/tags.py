# -*- coding: utf-8 -*-
"""
    qiita.tags
    ~~~~~~~~~~

    Wrapper for Qiita Tags.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client


class Tags(Client):
    def tag_items(self, url_name, params=None):
        """Get specific tag post.

        :param url_name:
        :param params:
        """
        params = {} if params is None else params

        return self.get('/tags/{0}/items'.format(url_name), params)

    def tags(self, params=None):
        """Get tag list.

        :param params:
        """
        params = {} if params is None else params

        return self.get('/tags', params)
