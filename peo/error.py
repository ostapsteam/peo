import logging
from flask import jsonify
from functools import wraps


log = logging.getLogger(__file__)


class Errors:
    errors = {}

    @classmethod
    def register(cls, errs):
        cls.errors.update(errs)

    @classmethod
    def get_resp(cls, err):
        for error, message in cls.errors.items():
            if isinstance(err, error):
                return message, message["status"]
        raise err

    @classmethod
    def handle_errors(cls, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                err, status = cls.get_resp(exc)
                return jsonify(err), status
        return wrap
