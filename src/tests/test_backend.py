import unittest

from app import create_app, db
from app.database.db_helper import reset
from flask import url_for


class BackendTest(unittest.TestCase):
    """
    A test model to help other tests related to forms and backend.
    Every operation in the test is under admin mode.
    """

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        reset(env="testing")

        # Admin data
        self.login_data = {"username": "admin", "password": "123"}
        self.login()

    def tearDown(self) -> None:
        db.session.close()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)


class ReportFormTest(BackendTest):
    """
    In this test, we test whether report form behaves properly.
    """

    def test_ok(self):
        response = self.client.post(
            url_for("user.report_page"),
            data={
                "building": "3",
                "location": "None",
                "item": "8",
                "description": "None",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Successfully report.", response.data)

    def test_bad(self):
        response = self.client.post(
            url_for("user.report_page"),
            data={
                "building": "None",
                "location": "None",
                "item": "None",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)


class SystemBackendTest(BackendTest):
    """
    In this test, we test whether operations to system settings is available.
    """

    def test_ok(self):
        response = self.client.delete(
            url_for("admin.system_backend_page"),
            json={"category": "offices", "id": "1"},
        )
        self.assertEqual(response.status_code, 200)

    def test_method_not_allowed(self):
        response = self.client.get(url_for("admin.system_backend_page"))
        self.assertEqual(response.status_code, 405)

    def test_bad_request(self):
        response = self.client.post(
            url_for("admin.system_backend_page"),
            json={"category": "items", "value": "test_item"},
        )
        self.assertEqual(response.status_code, 400)  # because no office is provided


class ManageUserBackendTest(BackendTest):
    """
    In this test, we test whether user management is available.
    """

    def test_add_one_user_ok(self):
        response = self.client.post(
            url_for("admin.manage_user_page"),
            data={
                "form_name": "add_one",
                "username": "710000",
                "name": "test",
                "classnum": "1498",
                "password": "password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_add_duplicate_user(self):
        response = self.client.post(
            url_for("admin.manage_user_page"),
            data={
                "form_name": "add_one",
                "username": "user",
                "name": "user",
                "classnum": "1498",
                "password": "password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user", response.data)

    def test_add_one_user_bad(self):
        # Add admin but email is not provided.
        response = self.client.post(
            url_for("admin.manage_user_page"),
            data={
                "form_name": "add_one",
                "username": "710000",
                "name": "test",
                "classnum": "0",
                "password": "password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email is required for admin.", response.data)

    def test_delete_single_user_ok(self):
        response = self.client.delete(
            url_for("admin.manage_user_backend_page"),
            json={"type": "single", "user_id": 1},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_group_ok(self):
        response = self.client.delete(
            url_for("admin.manage_user_backend_page"),
            json={"type": "group", "upper": "410000", "lower": "419999"},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_group_bad(self):
        response = self.client.delete(
            url_for("admin.manage_user_backend_page"), json={"type": "group"}
        )
        self.assertEqual(response.status_code, 400)

    def test_backend_method_not_allowed(self):
        response = self.client.get(url_for("admin.manage_user_backend_page"))
        self.assertEqual(response.status_code, 405)

    def test_backend_bad_request(self):
        response = self.client.delete(
            url_for("admin.manage_user_backend_page"),
            json={},
        )
        self.assertEqual(response.status_code, 400)


class BackupBackendTest(BackendTest):
    """
    In this test, we test whether backup functions work.
    """

    def test_ok(self):
        # it can test whether backup works
        response = self.client.post(url_for("admin.backup_backend_page"))
        self.assertEqual(response.status_code, 200)

    def test_method_not_allowed(self):
        response = self.client.get(url_for("admin.backup_backend_page"))
        self.assertEqual(response.status_code, 405)

    def test_bad_request(self):
        response = self.client.delete(url_for("admin.backup_backend_page"), json={})
        self.assertEqual(response.status_code, 400)

    def test_not_exists_backup_file(self):
        response = self.client.get(
            url_for("admin.get_backup_file", filename="notexists")
        )
        self.assertEqual(response.status_code, 404)


class UserSettingTest(BackendTest):
    """
    In this test, we test whether the user setting page is ok.
    """

    def test_ok(self):
        response = self.client.post(
            url_for("user.user_setting_page"),
            data={"email": "test@test.com", "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"OK.", response.data)

    def test_bad(self):
        response = self.client.post(
            url_for("user.user_setting_page"),
            data={},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid.", response.data)

    def test_too_short_password(self):
        response = self.client.post(
            url_for("user.user_setting_page"),
            data={"email": "test@test.com", "password": "short"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password is too short (at least 6 characters).", response.data)
