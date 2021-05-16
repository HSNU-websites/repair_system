import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users

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

    def test_report_page(self):
        r = self.client.get(url_for("user.report_page"))
        self.assertTrue(r.status_code == 401)

    def test_dashboard_page(self):
        r = self.client.get(url_for("user.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_admin_dashboard_page(self):
        r = self.client.get(url_for("admin.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_system_page(self):
        r = self.client.get(url_for("admin.system_page"))
        self.assertTrue(r.status_code == 401)

    def test_system_modification_page(self):
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
        self.login_data = {"username": "user", "password": "123"}
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

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)

    def test_login(self):
        r = self.login()
        self.assertTrue(
            r.status_code == 302
        )  # After a user successfully login, he or she will be redirected.

    def test_report_page(self):
        with self.client:
            self.login()
            r = self.client.get(url_for("user.report_page"))
            self.assertTrue(r.status_code == 200)

    def test_dashboard_page(self):
        with self.client:
            self.login()
            r = self.client.get(url_for("user.dashboard_page"))
            self.assertTrue(r.status_code == 200)

    def test_admin_dashboard_page(self):
        with self.client:
            self.login()
            r = self.client.get(url_for("admin.dashboard_page"))
            self.assertTrue(r.status_code == 403)

    def test_system_page(self):
        with self.client:
            self.login()
            r = self.client.get(url_for("admin.system_page"))
            self.assertTrue(r.status_code == 403)

    def test_system_modification_page(self):
        with self.client:
            self.login()
            r = self.client.post(url_for("admin.system_modification_page"))
            self.assertTrue(r.status_code == 403)


# Admin privileges
class AdminAuthTest(NormalUserAuthTest):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.login_data = {"username": "admin", "password": "123"}
        self.test_admin = Users(
            "admin",
            "$pbkdf2-sha256$29000$ujfGeG.NUUpJaa1VijHmfA$15ZVKxgUPhTL0si.qXhmnR6/fm70SNtRJ6gnBCF/bXo",
            "Admin",
            0,
            email="admin@127.0.0.1",
            admin=True,
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
            r = self.client.get(url_for("admin.system_page"))
            self.assertTrue(r.status_code == 200)

    def test_system_modification_page(self):
        with self.client:
            self.login()
            r = self.client.post(
                url_for("admin.system_modification_page"),
                json={"category": "offices", "value": "test"},  # Test case
            )
            self.assertTrue(r.status_code == 200)
