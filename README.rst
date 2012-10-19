Qiita
=====

Python wrapper for Qiita API v1.

Installation
------------

.. code-block:: sh

  $ virtualenv --distribute qiita
  $ source qiita/bin/activate
  $ cd qiita
  $ pip install py-qiita


Usage
-----

Get user's items
~~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Items

  client = Items()
  items = client.user_items('heavenshell')


Get tag's items
~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Tags

  client = Tags()
  items = cient.tag_items('python')

Get a specified item with comments and raw markdown content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Items

  client = Items()
  item_uuid = '1234567890abcdefg'
  items = cient.item(item_uuid)


Authenticated requests
----------------------

Login with "username & password" or "token"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Client

  client = Client(url_name='heavenshell', password='mysecret')
  token = client.token # => contains token
  # or
  client = Client(token='myauthtoken')

Get my items
~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Items

  client = Client(token='myauthtoken')
  items = client.user_item()

Post/Update/Delete an item
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Items

  client = Client(token='myauthtoken')
  params = {
    'title': 'Hello',
    'body': 'markdown text',
    'tags': [{ name: 'python', versions: ['2.6', '2.7'] }],
    'private': False
  }
  # post
  item = client.post_item(params)

  # update
  params['title'] = 'modified'
  cient.update_item(item['uuid'], params)

  # delete
  cient.delete_item(item['uuid'])


Stock/Unstock item
~~~~~~~~~~~~~~~~~~

.. code-block:: python

  # -*- coding: utf-8 -*-
  from qiita import Items

  client = Items(token='myauthtoken')
  item_uuid = '1489e2b291fed74713b2'
  # Stock
  client.stock_item(item_uuid)

  # Unstock
  client.unstock_item(item_uuid)

Contributing
------------
1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request
