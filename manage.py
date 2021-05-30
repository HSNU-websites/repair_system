import unittest
from datetime import datetime, timedelta
import random

from flask_script import Manager

import app.database.backup as b
import app.database.db_helper as h
import app.mail_helper as m
import db_default
from app import create_app, db
from app.database.model import Users, Buildings, Items, Offices, Records, Revisions, Statuses, timeformat

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
            is_valid=False,
            is_marked_deleted=True
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
            is_admin=True,
        ),
        Users.new(
            username="user",
            password="123",
            name="User",
            classnum=0,
        ),
    ]
    db.session.add_all(users)
    random_users = [
        Users.new(
            username=str(410001 + i),
            name="Student" + str(i),
            classnum=1300 + (i // 26)
        )
        for i in range(1000)
    ]
    db.session.add_all(random_users)

    # Buildings default
    db.session.add(Buildings(id=1, description="其他", sequence=len(db_default.buildings) + 1))
    for i, building in enumerate(db_default.buildings, start=1):
        db.session.add(Buildings.new(building, sequence=i))

    # Statuses default
    db.session.add(Statuses(id=1, description="其他", sequence=len(db_default.statuses) + 1))
    for i, status in enumerate(db_default.statuses, start=1):
        db.session.add(Statuses.new(status, sequence=i))

    # Offices default
    for i, office in enumerate(db_default.offices, start=1):
        db.session.add(Offices.new(office, sequence=i))

    db.session.commit()

    # Items default
    db.session.add(Items(id=1, description="其他", office_id=1, sequence=len(db_default.items) + 1))
    for i, item in enumerate(db_default.items, start=1):
        db.session.add(Items.new(item[0], item[1], sequence=i))
    db.session.commit()

    current_timestamp = int((datetime.now() - timedelta(days=10)).timestamp())
    count = 1000
    rt = random.sample(range(current_timestamp), k=count)
    rt.sort()
    random_records = [
        Records.new(
            user_id=random.randint(1, len(users) + len(random_users) + 1),
            item_id=random.randint(1, len(db_default.items) + 1),
            building_id=random.randint(1, len(db_default.buildings) + 1),
            location="某{}個地方".format(random.randint(1, 100000)),
            description="{}的紀錄".format(random.randint(1, 100000)),
            insert_time=datetime.fromtimestamp(random_timestamp).strftime(timeformat)
        )
        for random_timestamp in rt
    ]
    random_records += [
        Records.new(1, 1, 1, "某個地方", "十天前的紀錄", insert_time=(
            datetime.now() - timedelta(days=10)).strftime(timeformat)),
        Records.new(1, 1, 1, "某個地方", "三天前的紀錄", insert_time=(
            datetime.now() - timedelta(days=3)).strftime(timeformat)),
        Records.new(1, 1, 1, "某個地方", "昨天的紀錄", insert_time=(
            datetime.now() - timedelta(days=1)).strftime(timeformat)),
        Records.new(1, 1, 1, "某個地方", "今天的紀錄")
    ]
    db.session.bulk_save_objects(random_records)
    db.session.commit()

    random_revisions = [
        Revisions.new(
            record_id=random.randint(1, len(random_records)),
            user_id=random.randint(1, len(users) + 1),
            status_id=1,
            description="測試修訂{}紀錄".format(random.randint(1, 100000)),
        )
        for _ in range(500)
    ]
    random_revisions += [
        Revisions.new(
            record_id=random.randint(1, len(random_records)),
            user_id=random.randint(1, len(users) + 1),
            status_id=2,
            description="測試修訂{}紀錄".format(random.randint(1, 100000)),
        )
        for _ in range(200)
    ]
    db.session.bulk_save_objects(random_revisions)
    db.session.commit()

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
