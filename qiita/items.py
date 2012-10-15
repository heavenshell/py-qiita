# -*- coding: utf-8 -*-
"""
    qiita.items
    ~~~~~~~~~~~

    Qiita items.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client


class Items(Client):
    def post_item(self, params):
        return self.request('post', '/items', params)

    def update_item(self, uuid, params):
        return self.request('put', '/items/{0}'.format(uuid), params)

    def delete_item(self, uuid):
        return self.request('delete', '/items/{0}'.format(uuid))

    def item(self, uuid):
        """Get newest post.

        If authorized, get user's post otherwise public newest post.

        :param uuid:
        """
        return self.request('get', '/items/{0}'.format(uuid))

    def search_items(self, query, params=None):
        """search_items

        :param query:
        :param params:
        """
        if params is None:
            params = {'q': query}
        else:
            params['q'] = query

        return self.request('get', '/search', params)

    def stock_item(self, uuid):
        """Get user's stock.

        :param uuid:
        """
        return self.request('put', '/items/{0}/stock'.format(uuid))

    def unstock_item(self, uuid):
        """Unstock item.

        :param uuid:
        """
        return self.request('delete', '/items/{0}/stock'.format(uuid))
