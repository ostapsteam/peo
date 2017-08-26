import uuid

from peo.models.lab import Lab
from tests import DBTestCase


class LabModelTestCase(DBTestCase):

    def setUp(self):
        super().setUp()

    def test_lab_get(self):
        session = self.db_session()

        name = "Lab1"
        desc = "Test desc"

        lab1 = Lab(
            name=name,
            desc=desc
        )
        session.add(lab1)
        session.flush()

        self.assertIsNotNone(lab1.id)

        lab2 = Lab.get_by_name(session, lab1.name)

        self.assertEqual(lab1.id, lab2.id)

        with self.assertRaises(Lab.DoesNotExist):
            Lab.get(session, 0)

    def test_get_by_name(self):
        session = self.db_session()

        name = "Lab1"
        desc = "Test desc"

        lab1 = Lab(
            name=name,
            desc=desc
        )
        session.add(lab1)
        session.flush()

        self.assertIsNotNone(lab1.id)

        lab2 = Lab.get(session, lab1.id)

        self.assertEqual(lab1.id, lab2.id)

        self.assertIsNone(Lab.get_by_name(session, str(uuid.uuid4())))
