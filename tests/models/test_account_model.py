import uuid

from peo.db import DB
from peo.models.account import Account
from tests import DBTestCase


class AccountModelTestCase(DBTestCase):

    def setUp(self):
        super().setUp()

    def test_get(self):
        login = "user1"
        passwd = "passwd"

        with DB.session() as session:
            account1 = Account.create(session, login, passwd)
            session.add(account1)

        self.assertIsNotNone(account1.id)

        with DB.session() as session:
            user2 = Account.get(session, account1.id)
            self.assertEqual(account1.id, user2.id)

        with self.assertRaises(Account.DoesNotExist):
            Account.get(session, 0)

    def test_get_by_login(self):
        login = "user1"
        passwd = "passwd"

        with DB.session() as session:
            account1 = Account.create(session, login, passwd)
            session.add(account1)

        self.assertIsNotNone(account1.id)

        with DB.session() as session:
            user2 = Account.get_by_login(session, account1.login)
            self.assertEqual(account1.id, user2.id)
            self.assertIsNone(Account.get_by_login(session, str(uuid.uuid4())))

    def test_check_login_and_password(self):
        login = "user1"
        passwd = "passwd"

        with DB.session() as session:
            with self.assertRaises(Account.IncorrectLoginOrPassword):
                Account.check_login_and_password(session, str(uuid.uuid4()), str(uuid.uuid4()))

            Account.create(session, login, passwd)

        with DB.session() as session:
            Account.check_login_and_password(session, login, passwd)

            with self.assertRaises(Account.IncorrectLoginOrPassword):
                Account.check_login_and_password(session, login, str(uuid.uuid4()))
                Account.check_login_and_password(session, str(uuid.uuid4()), passwd)
