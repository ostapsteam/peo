from functools import wraps

from flask import jsonify, request, session, g
from marshmallow import Schema,fields
from peo.models.account import Account
from werkzeug.wrappers import Response


def get_error_resp(exc_dict):
    return jsonify(exc_dict), exc_dict["status"]


def process_request(f, *args, input_schema=None, output_schema=None, **kwargs):
    content = request.get_json(silent=False)
    if input_schema:
        req, errors = input_schema.load(content)
        if errors:
            return get_error_resp({
                "message": "Bad request",
                "status": 400,
                "errors": errors
            })
        resp = f(req, *args, **kwargs)
    else:
        resp = f(*args, **kwargs)
    if isinstance(resp, Response):
        return resp
    body, status = resp
    if output_schema:
        body, errors = output_schema.dump(body)
        if errors:
            return get_error_resp({
                "message": "Marshal error",
                "status": 500,
                "errors": errors
            })

    return jsonify(body), status


def validate(input_schema=None, output_schema=None):
    def decor(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            return process_request(
                f, *args, input_schema=input_schema, output_schema=output_schema, **kwargs)
        return wrap
    return decor


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'uid' in session:
            return f(*args, **kwargs)
        raise Account.Unauthorized
    return wrap


def with_common_errors(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Account.Unauthorized:
            return get_error_resp({
                "message": "Unauthorized",
                "status": 401
            })
    return wrap
