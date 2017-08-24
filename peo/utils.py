import json


def get_config(path):
    with open(path) as config_path:
        return json.load(config_path)