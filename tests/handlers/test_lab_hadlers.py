import json
import uuid

from peo.models.lab import Lab, LabSchema
from tests import RestTestCase


lab_schema = LabSchema()

class LabHandlersTestCase(RestTestCase):

    def setUp(self):
        super().setUp()

    def test_lab_hadler_get(self):
        session = self.db_session()

        resp = self.peo.get("/lab/0")
        self.assertEqual(resp.status_code, 404)

        name = "Lab1"
        desc = "Test desc"

        lab1 = Lab(
            name=name,
            desc=desc
        )
        session.add(lab1)
        session.flush()
        session.commit()

        resp = self.peo.get("/lab/{}".format(lab1.id))
        self.assertEqual(resp.status_code, 200)

        lab_resp = lab_schema.load(json.loads(resp.data)).data
        self.assertEqual(lab_resp["id"], lab1.id)
        self.assertEqual(lab_resp["name"], lab1.name)
        self.assertEqual(lab_resp["desc"], lab1.desc)

    def test_lab_hadler_post(self):
        lab1 = {
            "name": "Lab2",
            "desc": "Test desc2"
        }

        resp = self.peo.post("/labs", data=json.dumps(lab1), content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        lab_resp = lab_schema.load(json.loads(resp.data)).data
        self.assertIsNotNone(lab_resp["id"])
        self.assertEqual(lab_resp["name"], lab1["name"])
        self.assertEqual(lab_resp["desc"], lab1["desc"])

        lab2 = {
            "name": "Lab2",
            "desc": "Test desc333"
        }
        resp = self.peo.post("/labs", data=json.dumps(lab2), content_type="application/json")
        self.assertEqual(resp.status_code, 400)


    def test_lab_hadler_put(self):
        session = self.db_session()

        lab1 = {
            "name": "Lab1",
            "desc": "Test desc 1"
        }
        lab2 = {
            "name": "Lab2",
            "desc": "Test desc 2"
        }

        resp = self.peo.put("/lab/0", data=json.dumps(lab1), content_type="application/json")
        self.assertEqual(resp.status_code, 404)

        lab1obj = Lab(
            name=lab1["name"],
            desc=lab1["desc"]
        )
        lab2obj = Lab(
            name=lab2["name"],
            desc=lab2["desc"]
        )
        session.add_all([lab1obj, lab2obj])
        session.flush()
        session.commit()

        req = lab1.copy()
        req["name"] = lab2["name"]
        req["id"] = lab1obj.id

        resp = self.peo.put(
            "/lab/{}".format(lab1obj.id),
            data=json.dumps(req),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

        req["name"] = lab2["name"] + str(uuid.uuid4())

        resp = self.peo.put(
            "/lab/{}".format(lab1obj.id),
            data=json.dumps(req),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.peo.get("/lab/{}".format(req["id"]))
        self.assertEqual(resp.status_code, 200)

        lab_resp = lab_schema.load(json.loads(resp.data)).data
        self.assertEqual(lab_resp["id"], req["id"])
        self.assertEqual(lab_resp["name"], req["name"])
        self.assertEqual(lab_resp["desc"], req["desc"])

    def test_lab_hadler_delete(self):
        session = self.db_session()

        name = "Lab1"
        desc = "Test desc"

        lab1 = Lab(
            name=name,
            desc=desc
        )
        session.add(lab1)
        session.flush()
        session.commit()

        resp = self.peo.delete("/lab/{}".format(lab1.id))
        self.assertEqual(resp.status_code, 204)

        with self.assertRaises(Lab.DoesNotExist):
            Lab.get(self.db_session(), lab1.id)
