from os import path, mkdir
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, has_request_context, request
from flask_login import LoginManager

from .config import config
from .database import db

login_manager = LoginManager()


class LevelFilter(object):
    def __init__(self, level_1, level_2=None):
        self.level_1 = logging._checkLevel(level_1)
        if level_2:
            self.level_2 = logging._checkLevel(level_2)
        else:
            self.level_2 = None

    def filter(self, record):
        return record.levelno == self.level_1 or record.levelno == self.level_2


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[env])

    login_manager.init_app(app)
    db.init_app(app)

    if not path.exists("log"):
        mkdir("log")
    formatter = RequestFormatter(
        "[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s in %(module)s: %(message)s"
    )
    # access log
    access_log_handler = TimedRotatingFileHandler(
        r"log/access.log",
        when="D",
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=False,
        utc=True,
    )
    access_log_handler.setLevel("INFO")
    access_log_handler.setFormatter(formatter)
    access_log_handler.addFilter(LevelFilter("INFO", "WARNING"))
    # error log
    error_log_handler = TimedRotatingFileHandler(
        r"log/error.log",
        when="D",
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=False,
        utc=True,
    )
    error_log_handler.setLevel("ERROR")
    error_log_handler.setFormatter(formatter)

    app.logger.addHandler(access_log_handler)
    app.logger.addHandler(error_log_handler)

    # Blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    return app
