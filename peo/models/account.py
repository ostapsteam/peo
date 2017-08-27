from marshmallow import Schema, fields
from sqlalchemy import orm

from peo.models import Proto, Base
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash


class Account(Base, Proto):

    __tablename__ = "accounts"

    class DoesNotExist(Exception):
        pass

    class LoginAlreadyInUse(Exception):
        pass

    class IncorrectLoginOrPassword(Exception):
        pass

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    login = sa.Column(sa.String(128), nullable=False, unique=True)
    passwd_hash = sa.Column(sa.String(128), nullable=False)
    last_login = sa.Column(sa.DateTime)

    @staticmethod
    def create(session, login, password):
        account = Account(
            login=login,
            passwd_hash=generate_password_hash(password)
        )
        session.add(account)
        session.flush()
        return account

    @staticmethod
    def get(session, oid, with_deleted=False):
        account = session.query(Account).get(oid)
        if account and not (account.is_deleted() and not with_deleted):
            return account
        raise Account.DoesNotExist

    @staticmethod
    def get_by_login(session, login, with_deleted=False):
        result = session.query(Account).filter(
            Account.login == login
        )
        if not with_deleted:
            result = result.not_deleted(Account)
        return result.first()

    def set_password(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def set_login(self, login):
        if self.login != login:
            session = orm.object_session(self)
            assert session is not None, "Account has no attached session"
            another = Account.get_by_login(session, login)
            if another and another.id != self.id:
                raise Account.LoginAlreadyInUse
            self.login = login

    @staticmethod
    def check_login_and_password(session, login, password):
        account = Account.get_by_login(session, login)
        if account and account.check_password(password):
            return account
        raise Account.IncorrectLoginOrPassword


class AccountSchema(Schema):
    id = fields.Int()
    login = fields.Str(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime()
    last_login = fields.DateTime()
