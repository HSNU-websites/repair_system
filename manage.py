import unittest
from datetime import datetime, timedelta
from random import randint

from flask_script import Command, Manager

import app.database.backup as b
import app.database.db_helper as h
import app.mail_helper as m
import db_default
from app import create_app, db
from app.database.model import *

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

    db.session.add(
        Users.new(
            username="deleted",
            name="此帳號已刪除",
            classnum=0,
            valid=False
        )
    )
    # test users will be removed in production
    users = [
        Users.new(
            username="admin",
            password="123",
            name="Admin",
            classnum=0,
            email="admin@127.0.0.1",
            admin=True,
        ),
        Users.new(
            username="user",
            password="123",
            name="User",
            classnum=0,
            admin=False,
        ),
    ]
    db.session.add_all(users)

    # Statuses default
    db.session.add(Statuses("其他", sequence=len(db_default.statuses) + 1))
    for i, status in enumerate(db_default.statuses, start=1):
        db.session.add(Statuses(status, sequence=i))

    # Offices default
    for office in db_default.offices:
        db.session.add(Offices(office))

    db.session.commit()

    # Items default
    db.session.add(Items("其他", 1, sequence=len(db_default.items) + 1))
    for i, item in enumerate(db_default.items, start=1):
        db.session.add(Items(item[0], item[1], sequence=i))

    # Buildings default
    db.session.add(Buildings("其他", sequence=len(db_default.buildings) + 1))
    for i, building in enumerate(db_default.buildings, start=1):
        db.session.add(Buildings(building, sequence=i))

    db.session.commit()

    # "%Y-%m-%dT%H-%M-%S"
    current_timestamp = int(datetime.now().timestamp())
    random_records = [
        Records(
            user_id=randint(1, len(users)+1),
            item_id=randint(1, len(db_default.items) + 1),
            building_id=randint(1, len(db_default.buildings) + 1),
            location="某{}個地方".format(randint(1, 100000)),
            description="{}的紀錄".format(randint(1, 100000)),
            insert_time=datetime.fromtimestamp(
                randint(0, current_timestamp)).strftime(timeformat)
        )
        for _ in range(1000)
    ]
    records = [
        Records(1, 1, 1, "某個地方", "今天的紀錄"),
        Records(1, 1, 1, "某個地方", "昨天的紀錄", insert_time=(
            datetime.now() - timedelta(days=1)).strftime(timeformat)),
        Records(1, 1, 1, "某個地方", "三天前的紀錄", insert_time=(
            datetime.now() - timedelta(days=3)).strftime(timeformat)),
        Records(1, 1, 1, "某個地方", "十天前的紀錄", insert_time=(
            datetime.now() - timedelta(days=10)).strftime(timeformat))
    ]
    db.session.bulk_save_objects(random_records)
    db.session.add_all(records)

    db.session.commit()

    random_revisions = [
        Revisions(
            record_id=i,
            user_id=randint(1, len(users)+1),
            status_id=1,
            description="測試修訂{}紀錄".format(randint(1, 100000)),
        )
        for i in range(1, 20)
    ]
    random_revisions += [
        Revisions(
            record_id=i,
            user_id=randint(1, len(users)+1),
            status_id=2,
            description="測試修訂{}紀錄".format(randint(1, 100000)),
        )
        for i in range(1, 6)
    ]
    db.session.bulk_save_objects(random_revisions)
    db.session.add(Revisions(1, 1, 1, "測試修訂紀錄"))
    db.session.commit()

    # db.session.add(Unfinisheds(1))

    h.updateUnfinisheds()
    h.updateSequence()
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
