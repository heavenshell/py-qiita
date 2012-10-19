# -*- coding: utf-8 -*-
"""
    qiita.tests
    ~~~~~~~~~~~

    Tests for qiita library.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from unittest import TestCase


def settings():
    import os
    params = {'url_name': None, 'password': None}
    if 'QIITA_URL_NAME' in os.environ:
        params['url_name'] = os.environ['QIITA_URL_NAME']
    if 'QIITA_PASSWORD' in os.environ:
        params['password'] = os.environ['QIITA_PASSWORD']

    return params


class TestQiita(TestCase):
    def test_has_version(self):
        """ Qiita modlue has version. """
        from . import __version__
        self.assertEqual(__version__, '0.1')

    def test_has_json(self):
        """ Qiita modlue can load JSON library. """
        from . import json
        self.assertTrue(hasattr(json, 'dumps'))


class TestCient(TestCase):
    def setUp(self):
        from .client import Client
        self.params = settings()
        self.client = Client(**self.params)

    def test_rate_limit(self):
        """ Client should get rate limit. """
        result = self.client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])

    def test_init_options(self):
        """ Client should set options. """
        client = self.client
        self.assertEqual(client.url_name, self.params['url_name'])
        self.assertEqual(client.password, self.params['password'])

    def test_get_token(self):
        """ login should return token. """
        result = self.client.login()
        self.assertTrue('token' in result)

    def test_get_token_to_options(self):
        """ login should set token to token property. """
        result = self.client.login()
        self.assertEqual(self.client.token, result['token'])

    def test_should_set_requests_module(self):
        import requests
        from .client import Client
        client = Client(requests=requests)
        result = client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])


class TestItems(TestCase):
    def setUp(self):
        from .items import Items
        self.params = settings()
        self.items = Items(**self.params)
        self.items.login()
        self.params = {
            'title': u'Qiita Python library test.',
            'body': u'I love python!',
            'tags': [{'name': 'python', 'versions': ['2.6', '2.7']}],
            'private': False,
            'gist': False,
            'tweet': False
        }

    def test_post_item(self):
        """ Items should post new item. """
        result = self.items.post_item(self.params)
        self.assertEqual(result['title'], self.params['title'])

        # clean up
        self.items.delete_item(result['uuid'])

    def test_delete_item(self):
        """ Items should delete item. """
        post_result = self.items.post_item(self.params)

        result = self.items.delete_item(post_result['uuid'])
        self.assertEqual(result, '')

    def test_update_item(self):
        """ Items should update item. """
        post_result = self.items.post_item(self.params)
        self.params['title'] = u'Qiita Python library test update.'
        self.params['body'] = u'I love Python and Vim!'

        result = self.items.update_item(post_result['uuid'], self.params)
        self.assertEqual(result['title'], self.params['title'])

        # clean up
        self.items.delete_item(result['uuid'])

    def test_public_item(self):
        """ Items should get item without login. """
        from .items import Items
        client = Items()
        items = client.item('3288bf96ddc14bcef31c')
        self.assertTrue('body' in items)

    def test_search_items(self):
        """ Items should search items by query 'python'. """
        items = self.items.search_items(query='python')
        self.assertTrue('body' in items[0])

    def test_search_stock(self):
        """ Items should search stocked itmes by query. """
        params = {'stocked': 'true'}
        items = self.items.search_items(query='vim', params=params)
        self.assertTrue('body' in items[0])

    def test_stock_item(self):
        """ Items should stock post.  """
        stocked = self.items.stock_item('1489e2b291fed74713b2')
        self.assertEqual(stocked, '')

        # Clean up
        self.items.unstock_item('1489e2b291fed74713b2')

    def test_unstock_item(self):
        """ Items should unstock item. """
        self.items.stock_item('1489e2b291fed74713b2')

        stocked = self.items.unstock_item('1489e2b291fed74713b2')
        self.assertEqual(stocked, '')

    def test_should_raise_not_found_exception(self):
        """ Items should raise exception when there were no stocked item. """
        from .exceptions import NotFoundError
        try:
            self.items.unstock_item('1489e2b291fed74713b2')
            self.fail()
        except NotFoundError:
            self.assertTrue(True)
        except Exception:
            self.fail()


class TestTags(TestCase):
    def setUp(self):
        from .tags import Tags
        self.params = settings()
        self.tags = Tags()

    def test_tag_items(self):
        """ Tags should get items search by tag. """
        tags = self.tags.tag_items('python')
        self.assertTrue('body' in tags[0])
        self.assertTrue('uuid' in tags[0])

    def test_get_tags(self):
        """ Tags should get tags. """
        tags = self.tags.tags()
        self.assertTrue('name' in tags[0])
        self.assertTrue('url_name' in tags[0])


class TestUsers(TestCase):
    def setUp(self):
        from .users import Users
        self.params = settings()
        self.users = Users()

    def test_public_user_items(self):
        """ Users should return public items. """
        result = self.users.user_items()
        self.assertTrue(isinstance(result, list))

    def test_user_items(self):
        """ Users should return user's items. """
        result = self.users.user_items(self.params['url_name'])
        self.assertTrue(isinstance(result, list))

    def test_user(self):
        """ Users should get user info. """
        result = self.users.user(self.params['url_name'])
        self.assertTrue('url_name' in result)
        self.assertTrue('name' in result)

    def test_following_tags(self):
        """ Users should get following tags. """
        result = self.users.user_following_tags(self.params['url_name'])
        self.assertTrue('name' in result[0])
        self.assertTrue('url_name' in result[0])

    def test_user_following_users(self):
        """ Users should get following users. """
        result = self.users.user_following_users(self.params['url_name'])
        self.assertTrue('name' in result[0])
        self.assertTrue('url_name' in result[0])

    def test_user_stocks(self):
        """ Users should get stock. """
        result = self.users.user_stocks(self.params['url_name'])
        self.assertTrue('body' in result[0])

    def test_user_with_logged_in(self):
        """ Users should get user's info with sending token."""
        from .users import Users
        client = Users(**settings())
        client.login()
        result = client.user(self.params['url_name'])
        self.assertTrue('url_name' in result)
        self.assertTrue('name' in result)


class TestException(TestCase):
    def setUp(self):
        from .client import Client
        self.client = Client()

    def test_should_raise_not_found_exception(self):
        """ NotFound Error should be raised if user not exists. """
        from .exceptions import NotFoundError
        # with self.assertRaises() plays with Python2.7+
        try:
            self.client.get('/users/foobar')
            self.fail()
        except NotFoundError:
            self.assertTrue(True)
        except Exception:
            self.fail()
