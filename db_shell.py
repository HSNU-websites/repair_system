from flask import Flask
from flask_script import Manager, Server
from os import getenv
from database import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}".format(
    DB_USER=getenv("DB_USER"),
    DB_PASSWORD=getenv("DB_PASS"),
    DB_HOST=getenv("DB_HOST", "localhost"),
    DB_DATABASE=getenv("DB_NAME")
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
          "If you are sure, please type \'YES!\'")
    a = input()
    if a != "YES!":
        return 1

    db.drop_all()
    db.create_all()

    admin_users = [
        Users("william", "27b86ae4e3177308c786d57bbe6ddb52c056b510f33d159c56c1e026bdd8e81e",
              "william920429", 1502),
        Users("siriuskoan", "Invalid", "SiriusKoan", 1498)
    ]
    db.session.add_all(admin_users)
    # db.session.commit()

    # Items default
    db.session.add(Items("其他"))
    items = ["冷氣", "門窗鎖", "課桌椅", "桌機筆電", "投影機", "影印機",
             "廣播系統", "飲水機", "電話傳真", "電梯", "校園景觀"]
    for item in items:
        db.session.add(Items(item))

    # Buildings default
    db.session.add(Buildings("其他"))
    buildings = ["至善樓", "中正樓", "新民樓", "舊北樓", "東樓", "西樓", "中興堂", "技藝館", "圖書館", "室內體育館",
                 "體育組", "樂教館", "游泳池", "國中部", "學生社團活動中心", "室外籃球場", "排球場", "網球場", "操場"]
    for building in buildings:
        db.session.add(Buildings(building))

    db.session.commit()


if __name__ == "__main__":
    manager.run()
