import logging

from flask import current_app, flash, render_template, request
from flask_login import login_required

from ..database.db_helper import add_record, render_buildings, render_items
from ..forms import ReportForm
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
            building = form.building.data  # id
            location = form.location.data  # str
            item = form.item.data  # id
            description = form.description.data  # id
            add_record(building, location, item, description)
            flash("Successfully report.", "success")
            return render_template("report.html", form=form)
        else:
            current_app.logger.warning("POST /report: Invalid submit.")
            # Flask-wtf will return valid choice when the value is changed.
            for field, error in form.errors.items():
                for msg in error:
                    flash(msg, category="alert")
            return render_template("report.html", form=form)


@user_bp.route("/dashboard")
@login_required
def dashboard_page():
    pass
