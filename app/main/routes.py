from flask import render_template, url_for, redirect
from flask_login import current_user, UserMixin
from . import main_bp
from .. import login_manager

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(username):
    user = User()
    user.id = username
    return user

@main_bp.route("/", methods=["GET"])
def main_page():
    if current_user.is_active:
        return redirect(url_for(""))    # TODO
    else:
        return render_template("index.html")