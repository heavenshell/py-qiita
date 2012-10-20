# -*- coding: utf-8 -*-
"""
    qiita.exceptions
    ~~~~~~~~~~~~~~~~

    Qiita exceptions.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""


class QiitaException(Exception):
    pass


class BadRequestError(QiitaException):
    """ 400 error. """
    pass


class UnauthorizedError(QiitaException):
    """ 401 error. """
    pass


class ForbiddenError(QiitaException):
    """ 403 error. """
    pass


class NotFoundError(QiitaException):
    """ 404 error. """
    pass


class NotAcceptableError(QiitaException):
    """ 406 error. """
    pass


class UnprocessableEntityError(QiitaException):
    """ 422 error. """
    pass


class InternalServerError(QiitaException):
    """ 500 error. """
    pass


class ServiceUnavailableError(QiitaException):
    """ 503 error. """
    pass


def on_complte(status_code):
    if status_code == 400:
        raise BadRequestError()
    elif status_code == 401:
        raise UnauthorizedError()
    elif status_code == 403:
        raise ForbiddenError()
    elif status_code == 404:
        raise NotFoundError()
    elif status_code == 406:
        raise NotAcceptableError()
    elif status_code == 422:
        raise UnprocessableEntityError()
    elif status_code == 500:
        raise InternalServerError()
    elif status_code == 503:
        raise ServiceUnavailableError()


def error_message(response):
    pass
