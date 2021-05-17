import logging
from flask import current_app, flash, render_template, request
from flask_login import current_user, login_required
from ..database.db_helper import (
    add_record,
    render_buildings,
    render_items,
    render_records,
)
from ..forms import ReportForm
from ..mail_helper import send_report_mail
from . import user_bp


@user_bp.route("/report", methods=["GET", "POST"])
@login_required
def report_page():
    form = ReportForm()
    form.building.choices = render_buildings()
    form.item.choices = render_items()
    if request.method == "GET":
        current_app.logger.info("GET /report")
        return render_template("report.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /report")
            building_id = form.building.data  # type: int
            location = form.location.data  # type: str
            item_id = form.item.data  # type: int
            description = form.description.data  # type: str
            add_record(current_user.id, building_id, location, item_id, description)
            send_report_mail(
                current_user.id, building_id, location, item_id, description
            )
            flash("Successfully report.", "success")
            return render_template("report.html", form=form)
        else:
            current_app.logger.warning("POST /report: Invalid submit.")
            # Flask-wtf will return valid choice when the value is changed.
            for field, error in form.errors.items():
                for msg in error:
                    flash(msg, category="alert")
            return render_template("report.html", form=form)


@user_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    return render_template(
        # "user_dashboard.html", records=render_user_records(current_user.id)
    )
