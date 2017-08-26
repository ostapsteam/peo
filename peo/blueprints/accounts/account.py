from flask import Blueprint, request, jsonify, current_app

from peo.blueprints.labs.errors import handle_errors
from peo.db import DB
from peo.models.account import Account, AccountSchema

blue = Blueprint("accounts", __name__)


schema = AccountSchema()

@blue.route("/accounts", methods=["post"])
@handle_errors
def post():
    current_app.logger.info("Account create")
    content = request.get_json(silent=False)
    login = content["login"]
    password = content["password"]
    with DB.session() as db:
        account = Account.get_by_login(db, login)
        if account:
            raise Account.LoginAlreadyInUse
        account = Account.create(db, login, password)
        db.add(account)
        db.flush()
        return jsonify(schema.dump(account).data), 201


@blue.route("/account/<aid>", methods=["get"])
@handle_errors
def get(aid):
    current_app.logger.info("Account %s read" % aid)
    with DB.session() as db:
        account = Account.get(db, aid)
        return jsonify(schema.dump(account).data), 200


@blue.route("/account/<aid>", methods=["put"])
@handle_errors
def put(aid):
    current_app.logger.info("Account %s update" % aid)
    content = request.get_json(silent=False)
    login = content["login"]
    password = content["password"]
    with DB.session() as db:
        account = Account.get(db, aid)
        account.set_login(login)
        if password:
            account.set_password(password)
        db.flush()
        return jsonify(schema.dump(account).data), 200


@blue.route("/account/<aid>", methods=["delete"])
@handle_errors
def delete(aid):
    current_app.logger.info("Account %s delete" % aid)
    with DB.session() as db:
        account = Account.get(db, aid)
        account.delete()
        return "", 204


__all__ = "blue"