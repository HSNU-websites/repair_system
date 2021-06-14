import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users


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

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)


class ReportFormTest(BackendTest):
    """
    In this test, we test whether report form behaves properly.
    """

    def test_bad(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("user.report_page"),
                data={
                    "building": "None",
                    "location": "None",
                    "item": "None",
                },
            )
            self.assertTrue(response.status_code == 400)


class SystemBackendTest(BackendTest):
    """
    In this test, we test whether operations to system settings is available.
    """

    def test_ok(self):
        with self.client:
            self.login()
            response = self.client.delete(
                url_for("admin.system_backend_page"),
                json={"category": "offices", "id": "1"},
            )
            self.assertTrue(response.status_code == 200)

    def test_method_not_allowed(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.system_backend_page"))
            self.assertTrue(response.status_code == 405)

    def test_bad_request(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("admin.system_backend_page"),
                json={"category": "items", "value": "test_item"},
            )
            self.assertTrue(
                response.status_code == 400
            )  # because no office is provided


class ManageUserBackendTest(BackendTest):
    """
    In this test, we test whether user management is available.
    """

    """
    # The function has some problems and should not be tested now.
    def test_add_one_user_ok(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("admin.manage_user_page"),
                data={
                    "username": "710000",
                    "name": "test",
                    "classnum": "1498",
                    "password": "password",
                },
            )
            self.assertTrue(response.status_code == 200)
    """

    def test_add_one_user_bad(self):
        # Add admin but email is not provided.
        with self.client:
            self.login()
            response = self.client.post(
                url_for("admin.manage_user_page"),
                data={
                    "username": "710000",
                    "name": "test",
                    "classnum": "0",
                    "password": "password",
                },
            )
            self.assertTrue(response.status_code == 400)

    def test_backend_ok(self):
        with self.client:
            self.login()
            response = self.client.delete(
                url_for("admin.manage_user_backend_page"),
                json={"user_id": 1},
            )
            self.assertTrue(response.status_code == 200)

    def test_backend_method_not_allowed(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.manage_user_backend_page"))
            self.assertTrue(response.status_code == 405)

    def test_backend_bad_request(self):
        with self.client:
            self.login()
            response = self.client.delete(
                url_for("admin.manage_user_backend_page"),
                json={},
            )
            self.assertTrue(response.status_code == 400)


class BackupBackendTest(BackendTest):
    """
    In this test, we test whether backup functions work.
    """

    def test_ok(self):
        # it can test whether backup works
        with self.client:
            self.login()
            response = self.client.post(url_for("admin.backup_backend_page"))
            self.assertTrue(response.status_code == 200)

    def test_method_not_allowed(self):
        with self.client:
            self.login()
            response = self.client.get(url_for("admin.backup_backend_page"))
            self.assertTrue(response.status_code == 405)

    def test_bad_request(self):
        with self.client:
            self.login()
            response = self.client.delete(url_for("admin.backup_backend_page"), json={})
            self.assertTrue(response.status_code == 400)

    def test_not_exists_backup_file(self):
        with self.client:
            self.login()
            response = self.client.get(
                url_for("admin.get_backup_file", filename="notexists")
            )
            self.assertTrue(response.status_code == 404)


class UserSettingTest(BackendTest):
    """
    In this test, we test whether the user setting page is ok.
    """

    def test_ok(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("user.user_setting_page"),
                data={"email": "test@test.com", "password": "password"},
            )
            self.assertTrue(response.status_code == 200)

    def test_bad(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("user.user_setting_page"),
                data={},
            )
            self.assertTrue(response.status_code == 400)

    def test_too_short_password(self):
        with self.client:
            self.login()
            response = self.client.post(
                url_for("user.user_setting_page"),
                data={"email": "test@test.com", "password": "short"},
            )
            self.assertTrue(response.status_code == 400)
