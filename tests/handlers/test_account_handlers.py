import json
import uuid

from peo.db import DB
from peo.models.account import Account, AccountSchema
from tests import RestTestCase


account_schema = AccountSchema()


class AccountHandlersTestCase(RestTestCase):

    def setUp(self):
        super().setUp()

    def test_account_handler_get(self):
        resp = self.peo.get("/account/0")
        self.assertEqual(resp.status_code, 404)

        login = "account1"
        passwd = "password"

        with DB.session() as session:
            account1 = Account.create(session, login, passwd)
            session.add(account1)

        resp = self.peo.get("/account/{}".format(account1.id))
        self.assertEqual(resp.status_code, 200)

        account_resp = account_schema.load(json.loads(resp.data)).data
        self.assertEqual(account_resp["id"], account1.id)
        self.assertEqual(account_resp["login"], account1.login)

    def test_account_handler_post(self):
        account1 = {
            "login": "account1",
            "password": "password"
        }

        resp = self.peo.post("/accounts", data=json.dumps(account1), content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        account_resp = account_schema.load(json.loads(resp.data)).data
        self.assertIsNotNone(account_resp["id"])
        self.assertEqual(account_resp["login"], account1["login"])

        account2 = {
            "login": "account1",
            "password": "password2"
        }
        resp = self.peo.post("/accounts", data=json.dumps(account2), content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_account_handler_put(self):
        account1 = {
            "login": "account1",
            "password": "password1"
        }
        account2 = {
            "login": "account2",
            "password": "password2"
        }

        resp = self.peo.put("/account/0", data=json.dumps(account1), content_type="application/json")
        self.assertEqual(resp.status_code, 404)

        with DB.session() as session:
            account1obj = Account.create(session, **account1)
            Account.create(session, **account2)

        account1passwd = str(account1obj.passwd_hash)

        req = account1.copy()
        req["login"] = account2["login"]
        req["password"] = str(uuid.uuid4())
        req["id"] = account1obj.id

        resp = self.peo.put(
            "/account/{}".format(account1obj.id),
            data=json.dumps(req),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

        req["login"] = account2["login"] + str(uuid.uuid4())

        resp = self.peo.put(
            "/account/{}".format(account1obj.id),
            data=json.dumps(req),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        with DB.session() as session2:
            db_account = Account.get(session2, account1obj.id)
            self.assertNotEqual(account1["login"], db_account.login)
            self.assertNotEqual(account1passwd, db_account.passwd_hash)

    def test_lab_handler_delete(self):
        login = "account1"
        password = "password"

        with DB.session() as session:
            account1 = Account.create(session, login, password)

        resp = self.peo.delete("/account/{}".format(account1.id))
        self.assertEqual(resp.status_code, 204)

        with self.assertRaises(Account.DoesNotExist):
            Account.get(self.db_session(), account1.id)
