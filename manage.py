import unittest
from os import getenv
from time import sleep
from flask_script import Manager
from sqlalchemy.exc import OperationalError
from app.database.backup import backup
import app.database.db_helper as db_helper
from app import create_app, db
from app.database.model import Users
from app.mylogging import init_logging

app = create_app(getenv("ENV", "production"))
init_logging(app)
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
        if input() != "YES":
            print("Terminated.")
            return
    db_helper.reset(env=app.config["ENV"])


@manager.command
def backup():
    """
    Backup Tables
    """
    backup()


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def init_database():
    """
    Reset all Tables to Default if not initialized
    """
    max_try = 10
    sleep_sec = 5
    success = False
    for i in range(max_try):
        try:
            db.create_all()
        except OperationalError as e:
            print(f"Error: {e}")
            print(f"Failed to connect to database in try {i+1}, sleep for {sleep_sec} sec")
            sleep(sleep_sec)
        else:
            success = True
            break

    if success:
        print("Database connect successfully")
    else:
        raise RuntimeError(f"Could not connect to database after {max_try} tries")

    if Users.query.count() == 0:
        reset(yes=True)


@manager.command
def add_user():
    try:
        while True:
            username = input("帳號(學號)：")
            if username == "":
                print("帳號不可為空！")
            elif Users.username_exists(username):
                print("帳號已存在！")
            else:
                break
        while True:
            password = input("密碼：")
            if len(password) < 6:
                print("密碼須至少6碼！")
            else:
                break
        name = input("姓名：")
        admin = input("是否註冊為管理員？Y/N：")
        is_admin = (admin == "Y")

        user_info = {
            "username": username,
            "password": password,
            "name": name,
            "is_admin": is_admin
        }

        db_helper.add_users([user_info])
        print("使用者新增成功")

    except KeyboardInterrupt:
        print("\n操作取消")


if __name__ == "__main__":
    manager.run()
