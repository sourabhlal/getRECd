from bottle import response
from json import dumps


import collections
import functools


def json(f):
    """ A decorator that allows a bottle function to return a json object
    with the right content type. """

    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs)
        response.content_type = 'application/json'
        return dumps(rv)

    return wrapper


def safe(f):
    """ A decorator that creates a function to return a dict with success=True
    or success=False in case of failure. """

    def wrapper(*args, **kwargs):
        try:
            rv = f(*args, **kwargs)
            rv['success'] = True
            return rv
        except Exception as e:
            raise e
            response.status = 500
            return dict(success=False, message=str(e))

    return wrapper


def safe_json(f):
    """ A combination of the safe and json decorators """
    return json(safe(f))

class memoized(object):
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args, **kwargs):
        hargs = (args, tuple(kwargs.items()))

        # HACK: if we have more than 1000 items, clear the cache
        if len(self.memo) > 1000:
            self.memo = {}

        if hargs not in self.memo:
            self.memo[hargs] = self.fn(*args, **kwargs)
        return self.memo[hargs]