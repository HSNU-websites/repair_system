import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users


class ReportFormTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.login_data = {"username": "admin", "password": "123"}
        self.test_admin = Users(
            username="admin",
            password_hash="$pbkdf2-sha256$29000$ujfGeG.NUUpJaa1VijHmfA$15ZVKxgUPhTL0si.qXhmnR6/fm70SNtRJ6gnBCF/bXo",
            name="Admin",
            classnum=0,
            email="admin@127.0.0.1",
            admin=True,
        )
        db.session.add(self.test_admin)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def login(self):
        return self.client.post(url_for("main.index_page"), data=self.login_data)

    def test_report_page(self):
        with self.client:
            self.login()
            r = self.client.post(
                url_for("user.report_page"),
                data={
                    "building": "None",
                    "location": "None",
                    "item": "None",
                    "description": "None",
                },
            )
            self.assertTrue(r.status_code == 200)

    def test_system_modification_page_ok(self):
        with self.client:
            self.login()
            r = self.client.delete(
                url_for("admin.system_modification_page"),
                json={"category": "offices", "id": "1"},
            )
            self.assertTrue(r.status_code == 200)

    def test_system_modification_page_bad_request(self):
        with self.client:
            self.login()
            r = self.client.post(
                url_for("admin.system_modification_page"),
                json={"category": "items", "value": "test_item"},
            )
            self.assertTrue(r.status_code == 400)
