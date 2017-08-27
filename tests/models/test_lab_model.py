import uuid

from peo.db import DB
from peo.models.lab import Lab
from tests import DBTestCase


class LabModelTestCase(DBTestCase):

    def setUp(self):
        super().setUp()

    def test_lab_get(self):
        name = "Lab1"
        desc = "Test desc"

        with DB.session() as session:
            lab1 = Lab(
                name=name,
                desc=desc
            )
            session.add(lab1)
        self.assertIsNotNone(lab1.id)

        with DB.session() as session:
            lab2 = Lab.get(session, lab1.id)
            self.assertEqual(lab1.id, lab2.id)
            lab2.delete()

        with DB.session() as session:
            with self.assertRaises(Lab.DoesNotExist):
                Lab.get(session, lab1.id)

            with self.assertRaises(Lab.DoesNotExist):
                Lab.get(session, 0)

    def test_get_by_name(self):
        name = "Lab1"
        desc = "Test desc"

        with DB.session() as session:
            lab1 = Lab(
                name=name,
                desc=desc
            )
            session.add(lab1)

        self.assertIsNotNone(lab1.id)

        with DB.session() as session:
            lab2 = Lab.get_by_name(session, lab1.name)
            self.assertEqual(lab1.id, lab2.id)
            lab2.delete()

        with DB.session() as session:
            self.assertIsNone(Lab.get_by_name(session, lab1.name))
            self.assertIsNone(Lab.get_by_name(session, str(uuid.uuid4())))
