# -*- coding: utf-8 -*-
"""
    qiita.users
    ~~~~~~~~~~~

    Wrapper for Qiita users.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client


class Users(Client):
    def user_items(self, url_name=None, params=None):
        """Get user's item.

        :param url_name:
        :param params:
        """
        path = '/items' if url_name is None \
            else '/users/{0}/items'.format(url_name)
        params = {} if params is None else params

        return self.get(path, params)

    def user_following_tags(self, url_name, params=None):
        """Get user's following tags.

        :param url_name:
        :param params:
        """
        params = {} if params is None else params

        return self.get('/users/{0}/following_tags'.format(url_name), params)

    def user_following_users(self, url_name, params=None):
        """Get following users.

        :param url_name:
        :param params:
        """
        params = {} if params is None else params

        return self.get('/users/{0}/following_users'.format(url_name), params)

    def user_stocks(self, url_name=None, params=None):
        """Get user' stock.

        :param url_name:
        :param params:
        """
        path = '/stocks' if url_name is None \
            else '/users/{0}/stocks'.format(url_name)

        params = {} if params is None else params

        return self.get(path, params)

    def user(self, url_name=None):
        """Get user's info.

        :param url_name:
        """
        path = '/users' if url_name is None else '/users/{0}'.format(url_name)

        return self.get(path)
