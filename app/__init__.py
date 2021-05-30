from os import path, mkdir
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import (
    Flask,
    has_request_context,
    request,
    abort,
    flash,
    current_app,
    redirect,
    session,
)
from flask_login import LoginManager
from flask_login.utils import (
    login_url as make_login_url,
    expand_login_view,
    make_next_param,
)
from flask_login.signals import user_unauthorized
from flask_mail import Mail
from flask_apscheduler import APScheduler
from .config import config
from .database import db, cache


class LoginManager_(LoginManager):
    def __init__(self):
        super().__init__()

    def forbidden(self):
        user_unauthorized.send(current_app._get_current_object())

        if self.unauthorized_callback:
            return self.unauthorized_callback()

        if request.blueprint in self.blueprint_login_views:
            login_view = self.blueprint_login_views[request.blueprint]
        else:
            login_view = self.login_view

        if not login_view:
            abort(403)

        if self.login_message:
            if self.localize_callback is not None:
                flash(
                    self.localize_callback(self.login_message),
                    category=self.login_message_category,
                )
            else:
                flash(self.login_message, category=self.login_message_category)

        config = current_app.config
        if config.get("USE_SESSION_FOR_NEXT", USE_SESSION_FOR_NEXT):
            login_url = expand_login_view(login_view)
            session["_id"] = self._session_identifier_generator()
            session["next"] = make_next_param(login_url, request.url)
            redirect_url = make_login_url(login_view)
        else:
            redirect_url = make_login_url(login_view, next_url=request.url)

        return redirect(redirect_url)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


login_manager = LoginManager_()
mail = Mail()
scheduler = APScheduler()


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[env])

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    if app.config["ENV"] != "testing":
        scheduler.init_app(app)
        scheduler.start()
        from .mail_helper import send_daily_mail

        scheduler.add_job(
            "send_daily_mail",
            send_daily_mail,
            trigger="cron",
            day="*",
            hour="7",
        )

    # log
    if not path.exists("log"):
        mkdir("log")
    formatter = RequestFormatter(
        "[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s: %(message)s"
    )
    access_log_handler = TimedRotatingFileHandler(
        "log/access_" + datetime.now().strftime("%Y-%m-%d") + ".log",
        when="D",
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    access_log_handler.setLevel("INFO")
    access_log_handler.setFormatter(formatter)
    access_log_handler.suffix = "access_%Y-%m-%d.log"
    app.logger.addHandler(access_log_handler)

    # Blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    return app
