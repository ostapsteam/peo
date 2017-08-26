import argparse
import logging

from flask import Flask
from gunicorn.app.base import Application
from sqlalchemy import create_engine

from peo.blueprints.labs import lab
from peo.db import DB
from peo.error import Errors
from peo.utils import get_config

log = logging.getLogger(__file__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="config", help="Config file")
    parser.add_argument("--debug", dest="debug", help="Debug mode", action="store_true")
    args = parser.parse_args()

    log.info("Parse config file %s", args.config)
    config = get_config(args.config)
    DB.configure(engine=create_engine(config["database"]))
else:
    config = {}

app = Flask(__name__)
app.config.update(config)
app.register_blueprint(lab.blue)

Errors.register(lab.errors)


class PeoApplication(Application):
    def init(self, *args, **kwargs):
        return {
            'workers': config["workers"]
        }

    def load(self):
        return app


def main():
    if args.debug:
        log.info("Run in debug mode")
        app.run(debug=True)
    else:
        log.info("Run in war mode")
        PeoApplication().run()
