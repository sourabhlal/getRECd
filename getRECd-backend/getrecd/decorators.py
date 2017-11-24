from bottle import response
from json import dumps


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
            response.status_code = 500
            return dict(success=False, message=str(e))

    return wrapper


def safe_json(f):
    """ A combination of the safe and json decorators """
    return json(safe(f))
