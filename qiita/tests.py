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
        result = self.client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])

    def test_init_options(self):
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
    def test_items(self):
        """ Items should create. """
        from .items import Items
        self.items = Items()
        self.assertTrue(isinstance(self.items, Items))


class TestTags(TestCase):
    def test_tags(self):
        """ Tags should create. """
        from .tags import Tags
        self.tags = Tags()
        self.assertTrue(isinstance(self.tags, Tags))


class TestUsers(TestCase):
    def setUp(self):
         self.params = settings()

    def test_users(self):
        """ Users should create. """
        from .users import Users
        self.users = Users()
        self.assertTrue(isinstance(self.users, Users))

    def test_user_items(self):
        from .users import Users
        users = Users()
        result = users.user_items(self.params['url_name'])
        self.assertTrue(isinstance(result, list))
