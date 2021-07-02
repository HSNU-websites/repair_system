import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users
from app.database.db_helper import reset


class NoAuthTest(unittest.TestCase):
    """
    In this test, we test whether the website behaves appropriately when no user login.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # status code
        self.normal = 302
        self.admin = 302

    def tearDown(self) -> None:
        if self.app_context is not None:
            self.app_context.pop()

    def test_report_page(self):
        response = self.client.get(url_for("user.report_page"))
        self.assertEqual(response.status_code, self.normal)

    def test_dashboard_page(self):
        response = self.client.get(url_for("user.dashboard_page"))
        self.assertEqual(response.status_code, self.normal)

    def test_user_setting_page(self):
        response = self.client.get(url_for("user.user_setting_page"))
        self.assertEqual(response.status_code, self.normal)

    def test_admin_dashboard_page(self):
        response = self.client.get(url_for("admin.dashboard_page"))
        self.assertEqual(response.status_code, self.admin)

    def test_system_page(self):
        response = self.client.get(url_for("admin.system_page"))
        self.assertEqual(response.status_code, self.admin)

    def test_manage_user_page(self):
        response = self.client.post(url_for("admin.manage_user_page"))
        self.assertEqual(response.status_code, self.admin)

    def test_backup_page(self):
        response = self.client.post(url_for("admin.backup_page"))
        self.assertEqual(response.status_code, self.admin)


class NormalUserAuthTest(unittest.TestCase):
    """
    In this test, we test whether the website behaves appropriately when a normal student login.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.login_data = {"username": "user", "password": "123"}
        reset(is_test=True)
        # status code
        self.normal = 200
        self.admin = 302

    def tearDown(self) -> None:
        db.session.commit()
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)

    def test_login(self):
        response = self.login()
        self.assertEqual(
            response.status_code, 302
        )  # After a user successfully login, he or she will be redirected.

    def test_report_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("user.report_page"))
            self.assertEqual(response.status_code, self.normal)

    def test_dashboard_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("user.dashboard_page"))
            self.assertEqual(response.status_code, self.normal)

    def test_user_setting_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("user.user_setting_page"))
            self.assertEqual(response.status_code, self.normal)

    def test_admin_dashboard_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.dashboard_page"))
            self.assertEqual(response.status_code, self.admin)

    def test_system_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.system_page"))
            self.assertEqual(response.status_code, self.admin)

    def test_manage_user_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.manage_user_page"))
            self.assertEqual(response.status_code, self.admin)

    def test_backup_page(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.backup_page"))
            self.assertEqual(response.status_code, self.admin)


class AdminAuthTest(NormalUserAuthTest):
    """
    In this test, we test whether the website behaves appropriately when an admin login.
    The test derives from `NormalUserAuthTest`
    """

    def setUp(self) -> None:
        db.drop_all()
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
        db.session.commit()
        # status code
        self.normal = 200
        self.admin = 200
