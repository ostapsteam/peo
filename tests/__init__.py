from tempfile import mktemp
from unittest import TestCase

from sqlalchemy import create_engine

from peo.db import DB


class DBTestCase(TestCase):

    def setUp(self):
        return
        self.DB = DB.configure(
            create_engine(mktemp())
        )