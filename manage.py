import unittest

from flask_script import Manager

import db_default
from app import create_app, db
from app.database import Users, Admins, Items, Buildings, Statuses

app = create_app("development")
manager = Manager(app)


@manager.shell
def shell():
    return globals()


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
        Users("admin", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3", "admin", 0)
    ]
    db.session.add_all(admin_users)
    db.session.commit()  # id will be valid only after commit
    for user in admin_users:
        user.admin = Admins(user.id)

    # Statuses default
    db.session.add(Statuses("其他", len(db_default.statuses)+1))
    i = 0
    for status in db_default.statuses:
        db.session.add(Statuses(status, i := i+1))

    # Items default
    db.session.add(Items("其他", len(db_default.items)+1))
    i = 0
    for item in db_default.items:
        db.session.add(Items(item, i := i+1))

    # Buildings default
    db.session.add(Buildings("其他", len(db_default.buildings)+1))
    i = 0
    for building in db_default.buildings:
        db.session.add(Buildings(building, i := i+1))

    db.session.commit()


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
