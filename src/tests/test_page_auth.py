import unittest

from app import create_app, db
from app.database.db_helper import reset
from flask import url_for


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
        self.app_context = self.app.app_context()
        self.app_context.push()
        reset(env="testing")

        # NormalUser data
        self.login_data = {"username": "user", "password": "123"}
        self.login()

        # status code
        self.normal = 200
        self.admin = 302

    def tearDown(self) -> None:
        db.session.close()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)

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
        response = self.client.get(url_for("admin.manage_user_page"))
        self.assertEqual(response.status_code, self.admin)

    def test_backup_page(self):
        response = self.client.get(url_for("admin.backup_page"))
        self.assertEqual(response.status_code, self.admin)


class AdminAuthTest(NormalUserAuthTest):
    """
    In this test, we test whether the website behaves appropriately when an admin login.
    The test derives from `NormalUserAuthTest`
    """

    def setUp(self) -> None:
        super().setUp()

        # Admin data
        self.login_data = {"username": "admin", "password": "123"}
        self.client = self.app.test_client()
        self.login()

        # status code
        self.normal = 200
        self.admin = 200
