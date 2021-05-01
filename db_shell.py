from flask import Flask
from flask_script import Manager, Server
from os import getenv
from database import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}".format(
    DB_USER=getenv("DB_USER"),
    DB_PASSWORD=getenv("DB_PASSWORD"),
    DB_HOST=getenv("DB_HOST", "localhost"),
    DB_DATABASE=getenv("DB_DATABASE")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
manager = Manager(app)
manager.add_command("runserver", Server())


@manager.shell
def make_shell_context():
    return globals()


@manager.command
def reset():
    "Reset All Tables to Default."
    print("This will drop all tables.\n"
          "It's extremely dangerous.\n"
          "If you are sure, please type \"YES!\"")
    a = input()
    if a != "YES!":
        return 1

    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
