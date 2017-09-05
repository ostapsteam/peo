import json
import os
from tempfile import mktemp
from unittest import TestCase

import peo
from alembic.command import upgrade as upgrade_database
from alembic.config import Config
from peo.app import app
from peo.db import DB
from sqlalchemy import create_engine


class DBTestCase(TestCase):

    def setUp(self):
        self.__db_file = "sqlite:///" + mktemp()
        self.DB_URL = self.__db_file
        DB.configure(
            create_engine(self.DB_URL)
        )
        self.db_session = DB.Session

        MODULE_PATH = os.path.abspath(os.path.dirname(peo.__file__))
        config = Config(os.path.join(MODULE_PATH, 'alembic.ini'), 'alembic')
        #logging.getLogger('alembic.runtime.migration').disabled = True

        config.set_main_option('script_location', str(os.path.join(MODULE_PATH, 'alembic')))
        config.set_main_option('sqlalchemy.url', self.DB_URL)
        upgrade_database(config, 'head')

        super().setUp()

    def tearDown(self):
        if os._exists(self.__db_file):
            os.remove(self.__db_file)


class RestTestCase(DBTestCase):

    def setUp(self):
        self.peo = app
        self.peo.testing = True
        self.peo = self.peo.test_client()
        super().setUp()

    @classmethod
    def resp_to_json(cls, resp):
        return json.loads(resp.data.decode("utf-8"))

    def check_http_status(self, resp, status):
        self.assertEqual(resp.status_code, status, resp.data)