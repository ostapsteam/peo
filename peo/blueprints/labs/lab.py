from flask import Blueprint, current_app, redirect, url_for
from marshmallow import Schema, fields

from peo.blueprints import validate
from peo.blueprints.labs.errors import handle_errors
from peo.db import DB
from peo.models.lab import Lab, LabSchema

blue = Blueprint("labs", __name__)


class InputSchema(Schema):
    name = fields.Str(required=True)
    desc = fields.Str()


input_schema = InputSchema()
schema = LabSchema()


@blue.route("/labs", methods=["post"])
@handle_errors
@validate(input_schema=input_schema)
def post(content):
    current_app.logger.info("Lab create")
    name = content["name"]
    desc = content["desc"]
    with DB.session() as db:
        lab = Lab.get_by_name(db, name)
        if lab:
            raise Lab.NameAlreadyInUse
        lab = Lab(name=name, desc=desc)
        db.add(lab)
    return redirect(url_for('labs.get', lid=lab.id))


@blue.route("/lab/<lid>", methods=["get"])
@validate(output_schema=schema)
@handle_errors
def get(lid):
    current_app.logger.info("Lab %s read" % lid)
    with DB.session() as db:
        lab = Lab.get(db, lid)
        return lab, 200


@blue.route("/lab/<lid>", methods=["put"])
@handle_errors
@validate(input_schema=input_schema)
def put(content, lid):
    current_app.logger.info("Lab %s update" % lid)
    name = content["name"]
    desc = content["desc"]
    with DB.session() as db:
        lab = Lab.get(db, lid)
        lab.set_name(name)
        lab.desc = desc
    return redirect(url_for('labs.get', lid=lab.id))


@blue.route("/lab/<lid>", methods=["delete"])
@handle_errors
def delete(lid):
    current_app.logger.info("Lab %s delete" % lid)
    with DB.session() as db:
        lab = Lab.get(db, lid)
        lab.delete()
        return "", 204


__all__ = "blue"