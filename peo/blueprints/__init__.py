from functools import wraps

from flask import jsonify, request


def get_error_resp(exc_dict):
    return jsonify(exc_dict), exc_dict["status"]


def process_request(f, *args, input_schema=None, output_schema=None, **kwargs):
    content = request.get_json(silent=False)
    if input_schema:
        _, errors = input_schema.load(content)
        if errors:
            return get_error_resp({
                "message": "Bad request",
                "status": 400,
                "errors": errors
            })
        body, status = f(content, *args, **kwargs)
    else:
        body, status = f(*args, **kwargs)
    if output_schema:
        body, errors = output_schema.dump(body)
        if errors:
            return get_error_resp({
                "message": "Marshal error",
                "status": 500,
                "errors": errors
            })
        body = jsonify(body)
    return body, status


def validate(input_schema=None, output_schema=None):
    def decor(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            return process_request(
                f, *args, input_schema=input_schema, output_schema=output_schema, **kwargs)
        return wrap
    return decor