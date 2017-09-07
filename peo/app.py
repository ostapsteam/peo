import argparse
import logging
import os
import subprocess
import uuid

import time

import peo
from flask import Flask, g, jsonify
from gunicorn.app.base import Application
from peo.blueprints import get_error_resp
from sqlalchemy import create_engine

from peo.blueprints.labs import lab
from peo.blueprints.accounts import account
from peo.db import DB
from peo.utils import get_config

log = logging.getLogger(__file__)


app = Flask(__name__)
app.secret_key = app.config.get("secret_key", "default_key_21")


@app.before_request
def set_request_id():
    g.request_id = str(uuid.uuid4())


app.register_blueprint(lab.blue)
app.register_blueprint(account.blue)


@app.route("/", methods=["get"])
def app_info():
    return jsonify(name="peo", version=peo.VERSION)


@app.route("/travis/hook", methods=["post"])
def travis_hook():
    if "pid" not in app.config:
        return get_error_resp({
            "message": " Can't reload app. Pidfile wasn't set",
            "status": 400,
        })
    subprocess.check_call(["pip", "install", "peo", "--upgrade"])
    subprocess.check_call(["peo-database-manage", "--app-config", app.config["CURRENT_CONFIG"], "upgrade", "head"])
    with open(app.config["pid"]) as pidfile:
        os.kill(int(pidfile.read().strip()))
    return "", 204


class PeoApplication(Application):
    def init(self, *args, **kwargs):
        return {
            'workers': app.config["workers"],
            'pid': app.config["pid"]
        }

    def load(self):
        return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="config", help="Config file")
    parser.add_argument("--debug", dest="debug", help="Debug mode", action="store_true")
    args = parser.parse_args()

    log.info("Parse config file %s", args.config)
    app.config.update(get_config(args.config))
    app.config["CURRENT_CONFIG"] = args.config
    DB.configure(engine=create_engine(app.config["database"]))

    if args.debug:
        log.info("Run in debug mode")
        app.run(debug=True)
    else:
        log.info("Run in war mode")
        PeoApplication().run()