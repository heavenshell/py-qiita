# -*- coding: utf-8 -*-
"""
    qiita.tests
    ~~~~~~~~~~~

    Tests for qiita library.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from mock import patch
from unittest import TestCase


def settings():
    params = {'url_name': 'heavenshell', 'password': 'foobar'}

    return params


def dummy_response(m, filename=None):
    import os
    import requests
    response = requests.Response()
    response.status_code = 200
    if filename is None:
        response._content = ''
    else:
        filename = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
        with open(filename, 'r') as f:
            data = f.read()
            response._content = data

    m.return_value = response


def dummy_error_response(m, status_code):
    import requests
    from requests.exceptions import HTTPError
    response = requests.Response()
    response.status_code = status_code
    response._content = ''
    response.error = HTTPError

    m.return_value = response


class TestQiita(TestCase):
    def test_has_version(self):
        """ Qiita modlue has version. """
        from qiita import __version__
        self.assertEqual(__version__, '0.1')

    def test_has_json(self):
        """ Qiita modlue can load JSON library. """
        from qiita import json
        self.assertTrue(hasattr(json, 'dumps'))

    def test_shortcut(self):
        """ qiita should import Client, Items, Tags, Users. """
        from qiita import Client, Items, Tags, Users
        self.assertTrue(isinstance(Client(), Client))
        self.assertTrue(isinstance(Items(), Items))
        self.assertTrue(isinstance(Tags(), Tags))
        self.assertTrue(isinstance(Users(), Users))


class TestCient(TestCase):
    @patch('qiita.client.requests.post')
    def setUp(self, m):
        from qiita.client import Client
        dummy_response(m, 'data/auth.json')
        self.params = settings()
        self.client = Client(**self.params)

    @patch('qiita.client.requests.get')
    def test_rate_limit(self, m):
        """ Client should get rate limit. """
        dummy_response(m, 'data/rate_limit.json')
        result = self.client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])

    @patch('qiita.client.requests.get')
    def test_init_options(self, m):
        """ Client should set options. """
        dummy_response(m, 'data/rate_limit.json')
        client = self.client
        self.assertEqual(client.url_name, self.params['url_name'])
        self.assertEqual(client.password, self.params['password'])

    @patch('qiita.client.requests.post')
    def test_get_token(self, m):
        """ login should return token. """
        dummy_response(m, 'data/auth.json')
        result = self.client.login()
        self.assertTrue('token' in result)

    @patch('qiita.client.requests.post')
    def test_get_token_to_options(self, m):
        """ login should set token to token property. """
        dummy_response(m, 'data/auth.json')
        result = self.client.login()
        self.assertEqual(self.client.token, result['token'])

    @patch('qiita.client.requests.get')
    def test_should_set_requests_module(self, m):
        import requests
        from qiita.client import Client
        dummy_response(m, 'data/rate_limit.json')
        client = Client(requests=requests)
        result = client.rate_limit()
        self.assertEqual(result.keys(), ['limit', 'remaining'])

    def test_login_automatically(self):
        """ Client should get token when url_name and password set. """
        self.assertTrue(self.client.token is not None)

    @patch('qiita.client.requests.post')
    @patch('qiita.client.requests.get')
    def test_token_exists(self, m_get, m_post):
        """ Client should authorize when only token set. """
        from qiita.items import Items
        dummy_response(m_post, 'data/auth.json')
        client = Items(**self.params)
        token = client.token
        client = Items(token=token)

        dummy_response(m_get, 'data/search_item.json')
        params = {'stocked': 'true'}
        items = client.search_items(query='vim', params=params)
        self.assertTrue('body' in items[0])


class TestItems(TestCase):
    @patch('qiita.client.requests.post')
    def setUp(self, m):
        from qiita.items import Items
        dummy_response(m, 'data/auth.json')
        self.params = settings()
        self.items = Items(**self.params)
        self.params = {
            'title': u'Qiita Python library test.',
            'body': u'I love python!',
            'tags': [{'name': 'python', 'versions': ['2.6', '2.7']}],
            'private': False,
            'gist': False,
            'tweet': False
        }

    @patch('qiita.client.requests.post')
    def test_post_item(self, m):
        """ Items should post new item. """
        dummy_response(m, 'data/post_item.json')
        result = self.items.post_item(self.params)
        self.assertEqual(result['title'], self.params['title'])

    @patch('qiita.client.requests.delete')
    @patch('qiita.client.requests.post')
    def test_delete_item(self, mock_post, mock_delete):
        """ Items should delete item. """
        dummy_response(mock_post, 'data/post_item.json')
        post_result = self.items.post_item(self.params)

        dummy_response(mock_delete)
        result = self.items.delete_item(post_result['uuid'])
        self.assertEqual(result, '')

    @patch('qiita.client.requests.put')
    @patch('qiita.client.requests.post')
    def test_update_item(self, mock_post, mock_put):
        """ Items should update item. """
        dummy_response(mock_post, 'data/post_item.json')
        post_result = self.items.post_item(self.params)
        self.params['title'] = u'Qiita Python library test update.'
        self.params['body'] = u'I love Python and Vim!'

        dummy_response(mock_put, 'data/update_item.json')
        result = self.items.update_item(post_result['uuid'], self.params)
        self.assertEqual(result['title'], self.params['title'])

    @patch('qiita.client.requests.get')
    def test_public_item(self, m):
        """ Items should get item without login. """
        from qiita.items import Items
        dummy_response(m, 'data/public_items.json')
        client = Items()
        items = client.item('3288bf96ddc14bcef31c')
        self.assertTrue('body' in items)

    @patch('qiita.client.requests.get')
    def test_search_items(self, m):
        """ Items should search items by query 'python'. """
        dummy_response(m, 'data/search_items.json')
        items = self.items.search_items(query='python')
        self.assertTrue('body' in items[0])

    @patch('qiita.client.requests.get')
    def test_search_stock(self, m):
        """ Items should search stocked itmes by query. """
        dummy_response(m, 'data/search_items_stock.json')
        params = {'stocked': 'true'}
        items = self.items.search_items(query='vim', params=params)
        self.assertTrue('body' in items[0])

    @patch('qiita.client.requests.put')
    def test_stock_item(self, m):
        """ Items should stock post.  """
        dummy_response(m)
        stocked = self.items.stock_item('1489e2b291fed74713b2')
        self.assertEqual(stocked, '')

    @patch('qiita.client.requests.delete')
    def test_unstock_item(self, m):
        """ Items should unstock item. """
        dummy_response(m)
        stocked = self.items.unstock_item('1489e2b291fed74713b2')
        self.assertEqual(stocked, '')

    @patch('qiita.client.requests.delete')
    def test_should_raise_not_found_exception(self, m):
        """ Items should raise exception when there were no stocked item. """
        from qiita.exceptions import NotFoundError
        dummy_error_response(m, 404)
        try:
            self.items.unstock_item('1489e2b291fed74713b2')
            self.fail()
        except NotFoundError:
            self.assertTrue(True)
        except Exception:
            self.fail()


class TestTags(TestCase):
    def setUp(self):
        from qiita.tags import Tags
        self.tags = Tags()

    @patch('qiita.client.requests.get')
    def test_tag_items(self, m):
        """ Tags should get items search by tag. """
        dummy_response(m, 'data/tag_items.json')
        tags = self.tags.tag_items('python')
        self.assertTrue('body' in tags[0])
        self.assertTrue('uuid' in tags[0])

    @patch('qiita.client.requests.get')
    def test_get_tags(self, m):
        """ Tags should get tags. """
        dummy_response(m, 'data/tags.json')
        tags = self.tags.tags()
        self.assertTrue('name' in tags[0])
        self.assertTrue('url_name' in tags[0])


class TestUsers(TestCase):
    def setUp(self):
        from qiita.users import Users
        self.params = settings()
        self.users = Users()

    @patch('qiita.client.requests.get')
    def test_public_user_items(self, m):
        """ Users should return public items. """
        dummy_response(m, 'data/public_user_items.json')
        result = self.users.user_items()
        self.assertTrue(isinstance(result, list))

    @patch('qiita.client.requests.get')
    def test_user_items(self, m):
        """ Users should return user's items. """
        dummy_response(m, 'data/user_items.json')
        result = self.users.user_items(self.params['url_name'])
        self.assertTrue(isinstance(result, list))

    @patch('qiita.client.requests.get')
    def test_user(self, m):
        """ Users should get user info. """
        dummy_response(m, 'data/user_info.json')
        result = self.users.user(self.params['url_name'])
        self.assertTrue('url_name' in result)
        self.assertTrue('name' in result)

    @patch('qiita.client.requests.get')
    def test_following_tags(self, m):
        """ Users should get following tags. """
        dummy_response(m, 'data/user_following_tags.json')
        result = self.users.user_following_tags(self.params['url_name'])
        self.assertTrue('name' in result[0])
        self.assertTrue('url_name' in result[0])

    @patch('qiita.client.requests.get')
    def test_user_following_users(self, m):
        """ Users should get following users. """
        dummy_response(m, 'data/following_users.json')
        result = self.users.user_following_users(self.params['url_name'])
        self.assertTrue('name' in result[0])
        self.assertTrue('url_name' in result[0])

    @patch('qiita.client.requests.get')
    def test_user_stocks(self, m):
        """ Users should get stock. """
        dummy_response(m, 'data/user_stock.json')
        result = self.users.user_stocks(self.params['url_name'])
        self.assertTrue('body' in result[0])

    @patch('qiita.client.requests.post')
    @patch('qiita.client.requests.get')
    def test_user_with_logged_in(self, m_get, m_post):
        """ Users should get user's info with sending token."""
        from qiita.users import Users
        dummy_response(m_post, 'data/auth.json')
        client = Users(**settings())

        dummy_response(m_get, 'data/user_info.json')
        result = client.user(self.params['url_name'])
        self.assertTrue('url_name' in result)
        self.assertTrue('name' in result)


class TestException(TestCase):
    def setUp(self):
        from qiita.client import Client
        self.client = Client()

    @patch('qiita.client.requests.get')
    def test_should_raise_not_found_exception(self, m):
        """ NotFound Error should be raised if user not exists. """
        from qiita.exceptions import NotFoundError
        dummy_error_response(m, 404)
        # with self.assertRaises() plays with Python2.7+
        try:
            self.client.get('/users/foobar')
            self.fail()
        except NotFoundError:
            self.assertTrue(True)
        except Exception:
            self.fail()
