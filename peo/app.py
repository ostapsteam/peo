import argparse
import logging
from flask import Flask
from sqlalchemy import create_engine

from peo.blueprints.labs import lab
from peo.db import DB

from peo.error import Errors

log = logging.getLogger(__file__)

app = Flask(__name__)

DB.configure(engine=create_engine("postgresql://postgres:example@127.0.0.1/peo"))

app.register_blueprint(lab.labs_blue)

Errors.register(lab.errors)


if __name__ == "__main__":
    app.run(debug=True)
