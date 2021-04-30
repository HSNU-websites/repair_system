import unittest
from flask import url_for
from app import create_app


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_alive(self):
        r = self.client.get("main.index_page")
        self.assertTrue(r.status_code == 200)
