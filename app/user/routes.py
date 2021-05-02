from flask import request, render_template
from flask_login import login_required
from . import user_bp
from ..forms import ReportForm
from ..db_helper import render_buildings, render_items

@user_bp.route("/report", methods=["GET", "POST"])
def report_page():
    if request.method == "GET":
        form = ReportForm()
        form.building.choices = render_buildings()
        form.item.choices = render_items()
        return render_template("report.html", form=form)
    if request.method == "POST":
        # process report
        pass

@user_bp.route("/dashboard")
@login_required
def dashboard_page():
    pass