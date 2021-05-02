import unittest

from flask_script import Manager

import db_default
from app import create_app
from app import db
from app.database import Buildings
from app.database import Items
from app.database import Statuses
from app.database import Users

app = create_app("development")
manager = Manager(app)


@manager.shell
def shell():
    return dict(app=app, db=db)


@manager.command
def reset():
    """
    Reset All Tables to Default.
    """

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

    admin_users = [
        Users(
            "william",
            "27b86ae4e3177308c786d57bbe6ddb52c056b510f33d159c56c1e026bdd8e81e",
            "william920429",
            1502,
        ),
        Users("siriuskoan", "Invalid", "SiriusKoan", 1498),
    ]
    db.session.add_all(admin_users)
    # db.session.commit()

    # Statuses default
    db.session.add(Statuses("其他"))
    statuses = db_default.statuses
    for status in statuses:
        db.session.add(Statuses(status))

    # Items default
    db.session.add(Items("其他"))
    items = db_default.items
    for item in items:
        db.session.add(Items(item))

    # Buildings default
    db.session.add(Buildings("其他"))
    buildings = db_default.buildings
    for building in buildings:
        db.session.add(Buildings(building))

    db.session.commit()


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
