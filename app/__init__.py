from flask import (
    Flask,
    abort,
    current_app,
    flash, redirect,
    request,
    session
)
from flask_login import LoginManager
from flask_login.signals import user_unauthorized
from flask_login.utils import (
    expand_login_view,
    login_url as make_login_url,
    make_next_param,
)
from .config import config
from .database import cache, db
from .mail_helper import mail
from .scheduler_helper import scheduler


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


login_manager = LoginManager_()


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

    # Blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    return app
