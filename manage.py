import unittest
from os import getenv


from flask_script import Manager

import app.database.backup as b
import app.database.db_helper as h
from app import create_app, db
from app.database.model import Users

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
    h.reset(env=app.config["ENV"])


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


@manager.command
def init_database():
    """
    Reset all Tables to Default if not initialized
    """
    db.create_all()
    if Users.query.count() == 0:
        reset(yes=True)


if __name__ == "__main__":
    manager.run()
