# -*- coding: utf-8 -*-
"""
    qiita
    ~~~~~

    Qiita api wrapper for Python.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
try:
    import simplejson as json
except:
    import json

from .client import Client
from .items import Items
from .users import Users
from .tags import Tags


__version__ = '0.1.1'
__all__ = ['json', 'Client', 'Items', 'Users', 'Tags']
