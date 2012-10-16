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
    params = {'url_name': '', 'password': ''}
    if 'QIITA_URL_NAME' in os.environ:
        params['url_name'] = os.environ['QIITA_URL_NAME']
    if 'QIITA_PASSWORD' in os.environ:
        params['password'] = os.environ['QIITA_PASSWORD']

    return params


class TestQiita(TestCase):
    def test_has_version(self):
        """ Qiita modlue has version. """
        from . import __version__
        self.assertEquals(__version__, '0.1')

    def test_has_json(self):
        """ Qiita modlue can load JSON library. """
        from . import json
        self.assertTrue(hasattr(json, 'dumps'))


class TestCient(TestCase):
    def setUp(self):
        from .client import Client
        self.params = settings()
        self.client = Client(self.params)

    def test_client(self):
        """ Client should create. """
        from .client import Client
        self.assertTrue(isinstance(self.client, Client))

    def test_rate_limit(self):
        """ Client should get rate limit. """
        result = self.client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])

    def test_init_options(self):
        """ Client should set options. """
        client = self.client
        self.assertEquals(client.options['url_name'], self.params['url_name'])
        self.assertEquals(client.options['password'], self.params['password'])

    def test_get_token(self):
        """ login should return token. """
        result = self.client.login()
        self.assertTrue('token' in result)

    def test_get_token_to_options(self):
        """ login should set token to options property. """
        result = self.client.login()
        self.assertEquals(self.client.options['token'], result['token'])

class TestItems(TestCase):
    def setUp(self):
        from .items import Items
        self.params = settings()
        self.items = Items(self.params)
        self.items.login()

    def test_items(self):
        """ Items should create. """
        from .items import Items
        self.items = Items()
        self.assertTrue(isinstance(self.items, Items))

    def test_post_item(self):
        """ Items should post new item. """
        params = {
            'title': u'Qiita Python library test.',
            'body': u'I love python!',
            'tags': [{'name': 'python', 'versions': ['2.6', '2.7']}],
            'private': False,
            'gist': False,
            'tweet': False
        }
        result = self.items.post_item(params)
        self.assertEquals(result['title'], params['title'])


class TestTags(TestCase):
    def setUp(self):
        from .tags import Tags
        self.params = settings()
        self.tags = Tags()

    def test_tags(self):
        """ Tags should create. """
        from .tags import Tags
        self.assertTrue(isinstance(self.tags, Tags))

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

    def test_users(self):
        """ Users should create. """
        from .users import Users
        self.assertTrue(isinstance(self.users, Users))

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
        client = Users(settings())
        client.login()
        result = client.user(self.params['url_name'])
        self.assertTrue('url_name' in result)
        self.assertTrue('name' in result)
