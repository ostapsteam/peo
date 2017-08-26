from flask import jsonify


def get_error_resp(exc_dict):
    return jsonify(exc_dict), exc_dict["status"]