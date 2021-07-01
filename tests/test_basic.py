import unittest
from flask import url_for
from app import create_app


class BasicTest(unittest.TestCase):
    """
    In this test, we do some basic tests to determine whether the website behaves properly in normal situation.
    """

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
        response = self.client.get(url_for("main.index_page"))
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get("/wrong")
        self.assertEqual(response.status_code, 404)

    def test_blueprint(self):
        self.assertNotEqual(self.app.blueprints.get("main", None), None)
        self.assertNotEqual(self.app.blueprints.get("user", None), None)
        self.assertNotEqual(self.app.blueprints.get("admin", None), None)
