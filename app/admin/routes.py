from logging import NOTSET
from flask import request, render_template, current_app
from flask_login import login_required
from . import admin_bp
from ..database.db_helper import render_system_setting, delete, update, insert, render_all_records
from ..users import admin_required


@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page():
    if request.method == "GET":
        return render_template("admin_dashboard.html", records=render_all_records)
    if request.method == "POST":
        # form hasn't designed
        form = ""
        filter = form.filter.data
        return render_template("admin_dashboard.html", records=render_all_records(filter))

@admin_bp.route("/system", methods=["GET"])
@admin_required
@login_required
def system_page():
    if request.method == "GET":
        current_app.logger.info("GET /system")
        buildings, items, offices, statuses = render_system_setting()
        return render_template(
            "system.html",
            buildings=buildings,
            items=items,
            offices=offices,
            statuses=statuses,
        )


@admin_bp.route("/system_modification", methods=["POST", "DELETE", "UPDATE"])
@admin_required
@login_required
def system_modification_page():
    if request.method == "POST":
        # Add
        current_app.logger.info("POST /system_modification")
        data = request.get_json(force=True)
        if data.get("office") != None:
            args = {"description": data["value"], "office_id": data["office"]}
        else:
            args = {"description": data["value"]}
        if insert(data["category"], args):
            return "OK"
        else:
            return "Error", 400
    if request.method == "DELETE":
        # Delete
        current_app.logger.info("DELETE /system_modification")
        data = request.get_json(force=True)
        if delete(data["category"], data["id"]):
            return "OK"
        else:
            return "Error", 400
    if request.method == "UPDATE":
        # Update
        current_app.logger.info("UPDATE /system_modification")
        data = request.get_json(force=True)
        category = data[0]["category"]
        for r in data[1:]:
            if not update(
                category,
                {
                    "id": r["id"],
                    "description": r["description"],
                    "sequence": r["sequence"],
                },
            ):
                return "Error", 400
        return "OK"
