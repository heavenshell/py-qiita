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
        self.post('/items', params)

    def update_item(self, uuid, params):
        return self.put('/items/${uuid}'.format({'uuid': uuid}), params)

    def delete_item(self, uuid):
        return self.delete('/items/${uuid}'.format({'uuid': uuid}))

    def item(self, uuid):
        """Get newest post.

        If authorized, get user's post otherwise public newest post.

        :param uuid:
        """
        return self.get('/items/${uuid}'.format({'uuid': uuid}))

    def search_items(self, query, params=None):
        """search_items

        :param query:
        :param params:
        """
        if params is None:
            params = {'q': query}
        else:
            params['q'] = query

        return self.get('/search', params)

    def stock_item(self, uuid):
        """Get user's stock.

        :param uuid:
        """
        return self.put('/items/${uuid}/stock'.format({'uuid': uuid}))

    def unstock_item(self, uuid):
        """Unstock item.

        :param uuid:
        """
        return self.delete('/items/${uuid}/stock'.format({'uuid': uuid}))
