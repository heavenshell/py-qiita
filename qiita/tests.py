# -*- coding: utf-8 -*-
"""
    qiita.tests
    ~~~~~~~~~~~

    Tests for qiita library.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from unittest import TestCase


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
        self.client = Client()

    def test_client(self):
        """ Client should create. """
        from .client import Client
        self.assertTrue(isinstance(self.client, Client))

    def test_rate_limit(self):
        result = self.client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])


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
    def test_users(self):
        """ Users should create. """
        from .users import Users
        self.users = Users()
        self.assertTrue(isinstance(self.users, Users))
