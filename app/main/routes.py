from flask import redirect, render_template, request, url_for
from flask_login import UserMixin, current_user

from .. import login_manager
from ..forms import LoginForm
from . import main_bp


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(username):
    user = User()
    user.id = username
    return user


@main_bp.route("/", methods=["GET", "POST"])
def index_page():  # index page is login page
    if current_user.is_active:
        return redirect(url_for("user.report_page"))
    else:
        if request.method == "GET":
            return render_template("index.html", form=LoginForm())
        if request.method == "POST":
            # auth user
            pass
