from flask import Flask
from flask_restful import Api
from resources.lab import Lab
from db import DB
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

app = Flask(__name__)

DB.configure(
    create_engine(
        "sqlite:///db.sqlite",
        # pool_size=5,
        # pool=QueuePool,
    )
)

api = Api(app)

api.add_resource(Lab, '/lab/<id>')

if __name__ == "__main__":
    app.run(debug=True)
