from flask import (
    request,
    render_template,
    current_app,
    make_response,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
from . import admin_bp
from .helper import csv_handler
from ..forms import ReportsFilterForm, AddOneUserForm, AddUsersByFileForm, RestoreForm
from ..database.db_helper import (
    render_system_setting,
    render_records,
    render_users,
    add_users,
)
from ..database.backup_helper import get_backups, backup_dir
from ..users import admin_required


@admin_bp.route("/admin_dashboard/", methods=["GET", "POST"])
@admin_bp.route("/admin_dashboard/<int:page>", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page(page=1):
    """
    The page allows admins to browse all reports and make response to the reports.
    """
    # cookies are used to save filter when user turns page
    Filter = dict()
    if username := request.cookies.get("username"):
        Filter["username"] = username
    if classnum := request.cookies.get("classnum"):
        Filter["classnum"] = classnum
    form = ReportsFilterForm(**Filter)
    if request.method == "GET":
        current_app.logger.info("GET /admin_dashboard")
        return render_template(
            "admin_dashboard.html",
            records=render_records(Filter=Filter, page=page),
            form=form,
            statuses=render_system_setting()[3],
        )
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /admin_dashboard")
            cookies = []
            Filter = dict()
            if username := form.username.data:
                Filter["username"] = username
                cookies.append(("username", username))
            if classnum := form.classnum.data:
                Filter["classnum"] = classnum
                cookies.append(("classnum", classnum))

            response = make_response(redirect(url_for("admin.dashboard_page")))
            response.delete_cookie("username")
            response.delete_cookie("classnum")
            for cookie in cookies:
                response.set_cookie(*cookie, max_age=120)
            return response
        else:
            current_app.logger.warning("POST /admin_dashboard: Invalid submit")
            return redirect(url_for("admin.dashboard_page"))


@admin_bp.route("/system", methods=["GET"])
@admin_required
@login_required
def system_page():
    """
    The page allows admins to modify system setting. For example, they can add more buildings, offices and so on to the system.
    """
    current_app.logger.info("GET /system")
    buildings, items, offices, statuses = render_system_setting()
    return render_template(
        "system.html",
        buildings=buildings,
        items=items,
        offices=offices,
        statuses=statuses,
    )


@admin_bp.route("/manage_user/", methods=["GET", "POST"])
@admin_bp.route("/manage_user/<int:page>", methods=["GET", "POST"])
@admin_required
@login_required
def manage_user_page(page=1):
    """
    The page allows admins to add, edit and delete users.
    """
    form = AddOneUserForm()
    form_csv = AddUsersByFileForm()
    template = render_template(
        "manage_user.html",
        form=form,
        form_csv=form_csv,
        users=render_users(page=page),
    )
    if request.method == "GET":
        # Render all users
        current_app.logger.info("GET /manage_user")
        return template
    if request.method == "POST":
        # Add user
        if form.username.data:
            # Add one user
            if form.validate_on_submit():
                current_app.logger.info("POST /manage_user")
                data = {
                    "username": form.username.data,
                    "name": form.name.data,
                    "classnum": form.classnum.data,
                    "password": form.password.data,
                    "email": form.email.data,
                    "is_admin": int(form.classnum.data) == 0,
                }
                if already_exists := add_users([data]):
                    flash(", ".join(already_exists) + " 已經存在", category="warning")
                else:
                    flash("OK", category="success")
            else:
                for _, errorMessages in form.errors.items():
                    for err in errorMessages:
                        flash(err, category="alert")
                current_app.logger.warning("POST /manage_user: Invalid submit")
            return redirect(url_for("admin.manage_user_page"))
        if form_csv.csv_file.data:
            # Add users by csv
            if form_csv.validate_on_submit():
                current_app.logger.info("POST /manage_user")
                csv_file = form_csv.csv_file.data
                # data format: [{"username": "zxc", "name": "zxc", "password": "123", "classnum": "1400"}]
                if not (data := csv_handler(csv_file.read())):
                    flash("Bad encoding.", category="alert")
                else:
                    if already_exists := add_users(data):
                        flash(", ".join(already_exists) + " 已經存在", category="alert")
            else:
                current_app.logger.warning("POST /manage_user: Invalid submit")
                for _, errorMessages in form_csv.errors.items():
                    for err in errorMessages:
                        flash(err, category="alert")
            return redirect(url_for("admin.manage_user_page"))


@admin_bp.route("/backup", methods=["GET", "POST"])
@admin_required
@login_required
def backup_page():
    """
    The page allows admins to backup current database or restore from previous version.
    """
    form = RestoreForm()
    if request.method == "GET":
        return render_template("backup.html", form=form, backups=get_backups())
    if request.method == "POST":
        # save uploaded file
        if form.validate_on_submit():
            file = form.file.data
            file.save(backup_dir / file.filename)
            flash("Upload successfully.", category="success")
        else:
            for _, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, category="alert")
        return redirect(url_for("admin.backup_page"))
