from flask import Blueprint, request, jsonify, current_app

from peo.blueprints.labs.errors import handle_errors
from peo.db import DB
from peo.models.lab import Lab, LabSchema

blue = Blueprint("labs", __name__)

schema = LabSchema()

@blue.route("/labs", methods=["post"])
@handle_errors
def post():
    current_app.logger.info("Lab create")
    content = request.get_json(silent=False)
    name = content["name"]
    with DB.session() as db:
        lab = Lab.get_by_name(db, name)
        if lab:
            raise Lab.NameAlreadyInUse
        lab = Lab(
            name=name,
            desc=content["desc"]
        )
        db.add(lab)
        db.flush()
        return jsonify(schema.dump(lab).data), 201


@blue.route("/lab/<lid>", methods=["get"])
@handle_errors
def get(lid):
    current_app.logger.info("Lab %s read" % lid)
    with DB.session() as db:
        lab = Lab.get(db, lid)
        return jsonify(schema.dump(lab).data), 200


@blue.route("/lab/<lid>", methods=["put"])
@handle_errors
def put(lid):
    current_app.logger.info("Lab %s update" % lid)
    content = request.get_json(silent=False)
    name = content["name"]
    desc = content["desc"]
    with DB.session() as db:
        lab = Lab.get(db, lid)
        lab.set_name(name)
        lab.desc = desc
        db.flush()
        return jsonify(schema.dump(lab).data), 200


@blue.route("/lab/<lid>", methods=["delete"])
@handle_errors
def delete(lid):
    current_app.logger.info("Lab %s delete" % lid)
    with DB.session() as db:
        lab = Lab.get(db, lid)
        lab.delete()
        return "", 204


__all__ = "blue"