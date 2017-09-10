import argparse
import logging
import os
import signal
import uuid
from threading import Thread

import time

import peo
from alembic import command
from alembic.config import Config
from flask import Flask, g,current_app, jsonify, request
from gunicorn.app.base import Application
from peo.blueprints import get_error_resp
from peo.blueprints.accounts import account
from peo.blueprints.accounts.session_interface import ItsdangerousSessionInterface
from peo.blueprints.labs import lab
from peo.db import DB
from peo.utils import get_config
from sqlalchemy import create_engine

log = logging.getLogger(__file__)
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = app.config.get("secret_key", "default_key_21")
app.session_interface = ItsdangerousSessionInterface()


@app.before_request
def set_request_id():
    g.request_id = str(uuid.uuid4())


app.register_blueprint(lab.blue)
app.register_blueprint(account.blue)


class UpdateThread(Thread):

    def run(self):
        import pip
        time.sleep(10)
        pip.main(["install", "-U", "peo", "-i", "https://test.pypi.org/simple/", "--no-cache"])
        cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        cfg.set_main_option('script_location', str(os.path.join(BASE_PATH, 'alembic')))
        cfg.set_main_option('sqlalchemy.url', str(app.config['database']))
        command.upgrade(cfg, "head")

        with open(app.config["pid"]) as pidfile:
            os.kill(int(pidfile.read().strip()), signal.SIGHUP)


    @classmethod
    def getInstance(cls):
        if cls.thread is not None:
            return cls.thread


@app.route("/", methods=["get"])
def app_info():
    return jsonify(name="peo", version=peo.VERSION)


@app.route("/travisci", methods=["post", "get"])
def travis_hook():
    current_app.logger.info("Travis CI call from %s", request.remote_addr)
    # if request.remote_addr not in ("54.173.229.200", "54.175.230.252"):
    #     return get_error_resp({
    #         "message": "It's only for Travis",
    #         "status": 403,
    #     })
    if "pid" not in app.config:
        return get_error_resp({
            "message": " Can't reload app. Pidfile wasn't set",
            "status": 400,
        })

    UpdateThread().start()

    return "", 204


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

        class PeoApplication(Application):
            def init(self, *args, **kwargs):
                return {
                    'workers': app.config["workers"],
                    'pidfile': app.config["pid"]
                }

            def load(self):
                return app

        PeoApplication().run()