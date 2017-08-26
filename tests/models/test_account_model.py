import uuid

from peo.models.account import Account
from tests import DBTestCase


class AccountModelTestCase(DBTestCase):

    def setUp(self):
        super().setUp()

    def test_get(self):
        session = self.db_session()

        login = "user1"
        passwd = "passwd"

        account1 = Account.create(session, login, passwd)
        session.add(account1)
        session.flush()

        self.assertIsNotNone(account1.id)

        user2 = Account.get(session, account1.id)

        self.assertEqual(account1.id, user2.id)

        with self.assertRaises(Account.DoesNotExist):
            Account.get(session, 0)

    def test_get_by_login(self):
        session = self.db_session()

        login = "user1"
        passwd = "passwd"

        account1 = Account.create(session, login, passwd)
        session.add(account1)
        session.flush()

        self.assertIsNotNone(account1.id)

        user2 = Account.get_by_login(session, account1.login)

        self.assertEqual(account1.id, user2.id)

        self.assertIsNone(Account.get_by_login(session, str(uuid.uuid4())))
