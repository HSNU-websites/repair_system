import unittest

from flask_script import Manager, Command

import db_default
from app import create_app, db
from app.database import *
# import app.backup as b
import app.db_helper as h

app = create_app("development")
manager = Manager(app)


@manager.shell
def shell():
    return globals()


@manager.command
def reset(yes=False):
    """
    Reset all Tables to Default
    """

    if not yes:
        print(
            "This will drop all tables.\n"
            "It's extremely dangerous.\n"
            "If you are sure, please type 'YES'"
        )
        a = input()
        if a != "YES":
            print("Terminated.")
            return

    db.drop_all()
    db.create_all()

    db.session.add(Users("deleted", "", "此帳號已刪除", 0, valid=False))
    users = [
        Users(  # password: 123
            "admin",
            "$pbkdf2-sha256$29000$ujfGeG.NUUpJaa1VijHmfA$15ZVKxgUPhTL0si.qXhmnR6/fm70SNtRJ6gnBCF/bXo",
            "admin",
            0,
            admin=True,
        ),
        Users(  # password: 123
            "user",
            "$pbkdf2-sha256$29000$d06JESLk/L83xhijdA7BOA$foHk6yDuBg3vVwIBTH8Svg7WuIMZRjt6du036rlclAk",
            "user",
            0,
            admin=False,
        ),
    ]
    db.session.add_all(users)

    # Statuses default
    db.session.add(Statuses("其他", len(db_default.statuses) + 1))
    i = 0
    for status in db_default.statuses:
        db.session.add(Statuses(status, i := i + 1))

    # Items default
    db.session.add(Items("其他", len(db_default.items) + 1))
    i = 0
    for item in db_default.items:
        db.session.add(Items(item, i := i + 1))

    # Buildings default
    db.session.add(Buildings("其他", len(db_default.buildings) + 1))
    i = 0
    for building in db_default.buildings:
        db.session.add(Buildings(building, i := i + 1))

    db.session.add(Records(1, 1, 1, "某個地方", "測試報修紀錄"))
    db.session.add(Revisions(1, 1, 1, "測試修訂紀錄"))

    # db.session.add(Unfinished(1))

    h.updateUnfinished()

    db.session.commit()


@manager.command
def backup():
    """
    Backup Tables
    """
    b.backup()


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
