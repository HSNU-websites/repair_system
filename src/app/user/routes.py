from flask import current_app, flash, render_template, request, redirect
from flask.helpers import url_for
from flask_login import current_user, login_required
from ..database.db_helper import (
    add_record,
    render_buildings,
    render_items,
    render_records,
    get_user,
    update_users,
)
from ..forms import ReportForm, UserSettingForm
from ..mail_helper import send_report_mail
from . import user_bp


@user_bp.route("/report", methods=["GET", "POST"])
@login_required
def report_page():
    """
    The page allows students to report broken items.
    """
    form = ReportForm()
    form.building.choices = render_buildings()
    form.item.choices = render_items()
    if request.method == "GET":
        current_app.logger.info("GET /report")
        return render_template("report.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /report")
            building_id: int = form.building.data
            location: str = form.location.data
            item_id: int = form.item.data
            description: str = form.description.data
            add_record(current_user.id, building_id, location, item_id, description)
            send_report_mail(
                current_user.id, building_id, location, item_id, description
            )
            flash("Successfully report.", "success")
        else:
            current_app.logger.warning("POST /report: Invalid submit.")
            # Flask-wtf will return invalid choice when the value is changed.
            for _, error in form.errors.items():
                for msg in error:
                    flash(msg, category="alert")
        return redirect(url_for("user.report_page"))


# The page is student's dashboard, and he or she can browse all his or her reports here.
@user_bp.route("/dashboard/", methods=["GET"])
@user_bp.route("/dashboard/<int:page>", methods=["GET"])
@login_required
def dashboard_page(page=1):
    """
    The page is student's dashboard, and he or she can browse all his or her reports here.
    """
    current_app.logger.info("GET /dashboard")
    return render_template(
        "user_dashboard.html",
        records=render_records({"user_id": current_user.id}, page),
    )


@user_bp.route("/user_setting", methods=["GET", "POST"])
@login_required
def user_setting_page():
    """
    The page allows users, whether they are students or admins, to set their emails and passwords.
    """
    user = get_user(current_user.id)
    form = UserSettingForm(email=user["email"])
    if request.method == "GET":
        current_app.logger.info("GET /user_setting")
        return render_template("user_setting.html", user=user, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /user_setting")
            email = form.email.data
            password = form.password.data
            data = {"id": current_user.id, "email": email}
            if password != "":
                data["password"] = password
            update_users([data])
            flash("OK.", category="success")
        else:
            current_app.logger.warning("POST /user_setting: Invalid submit.")
            for _, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, category="alert")
        return redirect(url_for("user.user_setting_page"))
