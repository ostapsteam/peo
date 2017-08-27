from flask import Blueprint, current_app, redirect, url_for, session, abort
from marshmallow import Schema, fields

from peo.blueprints import validate
from peo.blueprints.accounts.errors import handle_errors
from peo.db import DB
from peo.models.account import Account, AccountSchema

blue = Blueprint("accounts", __name__)


class InputSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str()


input_schema = InputSchema()
schema = AccountSchema()


@blue.route("/accounts", methods=["post"])
@handle_errors
@validate(input_schema=input_schema)
def post(content):
    current_app.logger.info("Account create")
    login = content["login"]
    password = content["password"]
    with DB.session() as db:
        account = Account.get_by_login(db, login)
        if account:
            raise Account.LoginAlreadyInUse
        account = Account.create(db, login, password)
        db.add(account)
    return redirect(url_for('accounts.get', aid=account.id))


@blue.route("/account/<aid>", methods=["get"])
@handle_errors
@validate(output_schema=schema)
def get(aid):
    current_app.logger.info("Account %s read" % aid)
    with DB.session() as db:
        account = Account.get(db, aid)
        return account, 200


@blue.route("/account/<aid>", methods=["put"])
@handle_errors
@validate(input_schema=input_schema)
def put(content, aid):
    current_app.logger.info("Account %s update" % aid)
    login = content["login"]
    password = content["password"]
    with DB.session() as db:
        account = Account.get(db, aid)
        account.set_login(login)
        if password:
            account.set_password(password)
    return redirect(url_for('accounts.get', aid=account.id))


@blue.route("/account/<aid>", methods=["delete"])
@handle_errors
def delete(aid):
    current_app.logger.info("Account %s delete" % aid)
    with DB.session() as db:
        account = Account.get(db, aid)
        account.delete()
        return "", 204


@blue.route("/accounts/login", methods=["post"])
@handle_errors
@validate(input_schema=input_schema)
def login(content):
    if "uid" not in session:
        current_app.logger.info("Account login")
        login = content["login"]
        password = content["password"]
        with DB.session() as db:
            account = Account.check_login_and_password(db, login, password)
            session["uid"] = account.id
    return redirect(url_for('accounts.get', aid=session["uid"]))


@blue.route("/accounts/logout", methods=["get"])
@handle_errors
def logout():
    current_app.logger.info("Account logout")
    session.pop("uid", None)
    return "", 204


__all__ = "blue"
