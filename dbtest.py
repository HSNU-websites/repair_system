from flask import Flask
from flask_script import Manager
from flask_script import Server

from database import *
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{username}:{password}@localhost/{db_name}".format(
#     username=db_user, password=db_pass, db_name=db_name)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

manager = Manager(app)
# 設定 python manage.py runserver 為啟動 server 指令
manager.add_command("runserver", Server())
# 設定 python manage.py shell 為啟動互動式指令 shell 的指令


@manager.shell
def make_shell_context():
    return globals()


if __name__ == "__main__":
    manager.run()
