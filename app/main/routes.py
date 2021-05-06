from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_user, logout_user
from . import main_bp
from ..forms import LoginForm
from ..users import User
from ..db_helper import login_auth


@main_bp.route("/", methods=["GET", "POST"])
def index_page():  # index page is login page
    if current_user.is_active:
        current_app.logger.info("GET /: redirect")
        return redirect(url_for("user.report_page"))
    else:
        form = LoginForm()
        if request.method == "GET":
            current_app.logger.info("GET /")
            return render_template("index.html", form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                if user_data := login_auth(username, password):
                    current_app.logger.info("POST /: Login successfully.")
                    user = User()
                    user.id = user_data["id"]
                    login_user(user)
                    if user_data["isAdmin"]:
                        return redirect(url_for("admin.dashboard_page"))
                    else:
                        return redirect(url_for("user.report_page"))
                else:
                    current_app.logger.warning("POST /: Login failed.")
                    flash("Login failed.", category="alert")
                    return redirect(url_for("main.index_page"))
            else:
                current_app.logger.warning("POST /: Invalid submit.")
                flash("Invalid submit.", category="alert")
                return redirect(url_for("main.index_page"))


@main_bp.route("/logout", methods=["GET"])
def logout_page():
    current_app.logger.info("GET /logout")
    logout_user()
    flash("Logout.", category="info")
    return redirect(url_for("main.index_page"))
