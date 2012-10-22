# -*- coding: utf-8 -*-
"""
    qiita
    ~~~~~

    Qiita api wrapper for Python.

    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

app_name = 'qiita'

description = file(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(
    name=app_name,
    version='0.1.1',
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-qiita',
    description='Qiita api wrapper for Python',
    long_description=description,
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    install_requires=['simplejson', 'requests', 'mock'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    tests_require=['mock>=1.0.0'],
    test_suite='tests'
)
