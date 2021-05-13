import unittest

from flask import url_for, current_app

from app import create_app


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        if self.app_context is not None:
            self.app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(self.app.config["TESTING"])

    def test_alive(self):
        r = self.client.get(url_for("main.index_page"))
        self.assertTrue(r.status_code == 200)

    def test_404(self):
        r = self.client.get("/wrong")
        self.assertTrue(r.status_code == 404)

    def test_blueprint(self):
        self.assertTrue(self.app.blueprints.get("main", None))
        self.assertTrue(self.app.blueprints.get("user", None))
        self.assertTrue(self.app.blueprints.get("admin", None))
