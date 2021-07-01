import unittest
from os import getenv


from flask_script import Manager

import app.database.backup as b
import app.database.db_helper as h
import app.mail_helper as m
from app import create_app, db
from app.database.model import (
    Users,
    Buildings,
    Items,
    Offices,
    Records,
    Revisions,
    Statuses,
    timeformat,
)

app = create_app(getenv("ENV", "production"))
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
    is_development = app.config["ENV"] == "development"
    h.reset(is_development=is_development)


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


@app.before_first_request
def init_database():
    db.create_all()
    if Users.query.count() == 0:
        reset(True)


if __name__ == "__main__":
    manager.run()
