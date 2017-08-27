import argparse
import logging

from flask import Flask
from gunicorn.app.base import Application
from sqlalchemy import create_engine

from peo.blueprints.labs import lab
from peo.blueprints.accounts import account
from peo.db import DB
from peo.utils import get_config

log = logging.getLogger(__file__)


app = Flask(__name__)
app.secret_key = app.config.get("secret_key", "default_key_21")

app.register_blueprint(lab.blue)
app.register_blueprint(account.blue)


class PeoApplication(Application):
    def init(self, *args, **kwargs):
        return {
            'workers': app.config["workers"]
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
    DB.configure(engine=create_engine(app.config["database"]))

    if args.debug:
        log.info("Run in debug mode")
        app.run(debug=True)
    else:
        log.info("Run in war mode")
        PeoApplication().run()
