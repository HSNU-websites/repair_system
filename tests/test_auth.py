import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users


class NoAuthTest(unittest.TestCase):
    """
    In this test, we test whether the website behaves appropriately when no user login.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        if self.app_context is not None:
            self.app_context.pop()

    def test_report_page(self):
        response = self.client.get(url_for("user.report_page"))
        self.assertTrue(response.status_code == 401)

    def test_dashboard_page(self):
        response = self.client.get(url_for("user.dashboard_page"))
        self.assertTrue(response.status_code == 401)

    def test_admin_dashboard_page(self):
        response = self.client.get(url_for("admin.dashboard_page"))
        self.assertTrue(response.status_code == 401)

    def test_system_page(self):
        response = self.client.get(url_for("admin.system_page"))
        self.assertTrue(response.status_code == 401)

    def test_system_modification_page(self):
        response = self.client.post(url_for("admin.system_modification_page"))
        self.assertTrue(response.status_code == 401)


class NormalUserAuthTest(unittest.TestCase):
    """
    In this test, we test whether the website behaves appropriately when a normal student login.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.login_data = {"username": "user", "password": "123"}
        self.user = Users.new(
            username="user",
            password="123",
            name="User",
            classnum=0,
            is_admin=False,
        )
        db.session.add(self.user)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)

    def test_login(self):
        response = self.login()
        self.assertTrue(
            response.status_code == 302
        )  # After a user successfully login, he or she will be redirected.

    def test_report_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("user.report_page"))
            self.assertTrue(response.status_code == 200)

    def test_dashboard_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("user.dashboard_page"))
            self.assertTrue(response.status_code == 200)

    def test_admin_dashboard_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.dashboard_page"))
            self.assertTrue(response.status_code == 403)

    def test_system_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.system_page"))
            self.assertTrue(response.status_code == 403)

    def test_system_modification_page(self):
        with self.client:
            self.login()
            response = self.client.post(url_for("admin.system_modification_page"))
            self.assertTrue(response.status_code == 403)


class AdminAuthTest(NormalUserAuthTest):
    """
    In this test, we test whether the website behaves appropriately when an admin login.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.login_data = {"username": "admin", "password": "123"}
        self.test_admin = Users.new(
            username="admin",
            password="123",
            name="Admin",
            classnum=0,
            email="admin@127.0.0.1",
            is_admin=True,
        )
        db.session.add(self.test_admin)

    def test_admin_dashboard_page(self):
        with self.client:
            self.login()
            r = self.client.get(url_for("admin.dashboard_page"))
            self.assertTrue(r.status_code == 200)

    def test_system_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.system_page"))
            self.assertTrue(response.status_code == 200)

    def test_system_modification_page(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("admin.system_modification_page"),
                json={"category": "offices", "value": "test"},  # Test case
            )
            self.assertTrue(response.status_code == 200)
