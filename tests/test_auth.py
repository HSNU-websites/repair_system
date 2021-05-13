import unittest
from flask import url_for
from app import create_app, db
from app.database.model import Users


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.db = db
        self.db.create_all()

        self.test_user = Users(
            "user",
            "$pbkdf2-sha256$29000$d06JESLk/L83xhijdA7BOA$foHk6yDuBg3vVwIBTH8Svg7WuIMZRjt6du036rlclAk",
            "User",
            0,
            admin=False,
        )
        self.test_admin = Users(
            "admin",
            "$pbkdf2-sha256$29000$ujfGeG.NUUpJaa1VijHmfA$15ZVKxgUPhTL0si.qXhmnR6/fm70SNtRJ6gnBCF/bXo",
            "Admin",
            0,
            email="admin@127.0.0.1",
            admin=True,
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_no_user_auth_report_page(self):
        r = self.client.get(url_for("user.report_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_user_auth_dashboard_page(self):
        r = self.client.get(url_for("user.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_admin_auth_dashboard_page(self):
        r = self.client.get(url_for("admin.dashboard_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_admin_auth_system_page(self):
        r = self.client.get(url_for("admin.system_page"))
        self.assertTrue(r.status_code == 401)

    def test_no_admin_auth_system_modification_page(self):
        r = self.client.post(url_for("admin.system_modification_page"))
        self.assertTrue(r.status_code == 401)
