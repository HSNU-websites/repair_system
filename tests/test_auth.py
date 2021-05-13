import unittest
from flask import url_for
from flask_login import login_user, current_user
from app import create_app, db
from app.database.model import Users
from app.database.db_helper import login_auth

# No authentication
class NoAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        if self.app_context is not None:
            self.app_context.pop()

    def test_no_user_auth_report_page(self):
        r = self.client.get(url_for("user.report_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_user_auth_dashboard_page(self):
        r = self.client.get(url_for("user.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_user_auth_admin_dashboard_page(self):
        r = self.client.get(url_for("admin.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_user_auth_system_page(self):
        r = self.client.get(url_for("admin.system_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_user_auth_system_modification_page(self):
        r = self.client.post(url_for("admin.system_modification_page"))
        self.assertTrue(r.status_code == 401)


# Only normal student privileges
class NormalUserAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.user = Users(
            "user",
            "$pbkdf2-sha256$29000$d06JESLk/L83xhijdA7BOA$foHk6yDuBg3vVwIBTH8Svg7WuIMZRjt6du036rlclAk",
            "User",
            0,
            admin=False,
        )
        db.session.add(self.user)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def test_normal_user_auth_report_page(self):
        with self.client:
            self.client.post(
                url_for("main.index_page"), data={"username": "user", "password": "123"}
            )
            r = self.client.get(url_for("user.report_page"))
            self.assertTrue(r.status_code == 200)

    def test_normal_user_auth_dashboard_page(self):
        with self.client:
            self.client.post(
                url_for("main.index_page"), data={"username": "user", "password": "123"}
            )
            r = self.client.get(url_for("user.dashboard_page"))
            self.assertTrue(r.status_code == 200)

    def test_normal_user_auth_admin_dashboard_page(self):
        with self.client:
            self.client.post(
                url_for("main.index_page"), data={"username": "user", "password": "123"}
            )
            r = self.client.get(url_for("admin.dashboard_page"))
            self.assertTrue(r.status_code == 401)

    def test_normal_user_auth_system_page(self):
        with self.client:
            self.client.post(
                url_for("main.index_page"), data={"username": "user", "password": "123"}
            )
            r = self.client.get(url_for("admin.system_page"))
            self.assertTrue(r.status_code == 401)

    def test_normal_user_auth_system_modification_page(self):
        with self.client:
            self.client.post(
                url_for("main.index_page"), data={"username": "user", "password": "123"}
            )
            r = self.client.post(url_for("admin.system_modification_page"))
            self.assertTrue(r.status_code == 401)
