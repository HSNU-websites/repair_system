from flask import request, current_app, send_file, abort
from flask_login import login_required, current_user
from . import admin_bp
from ..users import admin_required
from ..database.db_helper import (
    delete,
    update,
    insert,
    del_users,
    update_users,
    add_revision,
    del_revisions,
    del_records,
)
from ..database.backup_helper import backup, restore, del_backup, backup_dir


@admin_bp.route("/admin_dashboard_backend", methods=["POST", "DELETE"])
@admin_required
@login_required
def admin_dashboard_backend_page():
    """
    The page receives the response to the report and the command to delete a report or a revision.
    """
    if request.method == "POST":
        data = request.get_json(force=True)
        add_revision(
            int(data["record_id"]),
            current_user.id,
            int(data["status_id"]),
            data["description"],
        )
        return "OK"
    if request.method == "DELETE":
        data = request.get_json(force=True)
        category = data["category"]
        id = int(data["id"])
        if category == "record":
            del_records([id])
        if category == "revision":
            del_revisions([id])
        return "OK"


@admin_bp.route("/system_backend", methods=["POST", "DELETE", "UPDATE"])
@admin_required
@login_required
def system_backend_page():
    """
    The page handles the system modification signals which are sent from `/system`.
    """
    if request.method == "POST":
        # Add
        current_app.logger.info("POST /system_backend")
        data = request.get_json(force=True)
        if data.get("office") != None:
            args = {"description": data["value"], "office_id": data["office"]}
        else:
            args = {"description": data["value"]}
        if insert(data["category"], args):
            return "OK"
        else:
            abort(400)
    if request.method == "DELETE":
        # Delete
        current_app.logger.info("DELETE /system_backend")
        data = request.get_json(force=True)
        if delete(data["category"], data["id"]):
            return "OK"
        else:
            abort(400)
    if request.method == "UPDATE":
        # Update
        current_app.logger.info("UPDATE /system_backend")
        data = request.get_json(force=True)
        category = data[0]["category"]
        for r in data[1:]:
            new = {
                "id": r["id"],
                "description": r["description"],
                "sequence": r["sequence"],
            }
            if r.get("office_id", None):
                new["office_id"] = r["office_id"]
            if not update(category, new):
                abort(400)
        return "OK"


@admin_bp.route("/manage_user_backend", methods=["DELETE", "UPDATE"])
@admin_required
@login_required
def manage_user_backend_page():
    """
    The page handles the request to delete and update user's information.
    """
    if request.method == "DELETE":
        # Delete user
        current_app.logger.info("DELETE /manage_user_backend")
        data = request.get_json(force=True)
        try:
            del_users([data["user_id"]])
            return "OK"
        except:
            abort(400)
    if request.method == "UPDATE":
        # Update user
        current_app.logger.info("UPDATE /manage_user_backend")
        data = request.get_json(force=True)
        try:
            update_users([data])
            return "OK"
        except:
            abort(400)


@admin_bp.route("/backup_backend", methods=["POST", "DELETE", "UPDATE"])
@admin_required
@login_required
def backup_backend_page():
    """
    The page handles the request to do some operations to backup system.
    """
    if request.method == "POST":
        # do backup
        try:
            backup()
            return "OK"
        except:
            abort(400)
    if request.method == "DELETE":
        # delete backup
        try:
            backup_name = request.get_json(force=True)["name"]
            del_backup(backup_name)
            return "OK"
        except:
            abort(400)
    if request.method == "UPDATE":
        # restore to specific version
        # NOT available to use now
        try:
            backup_name = request.get_json(force=True)["name"]
            restore(backup_name)
            return "OK"
        except:
            abort(400)


@admin_bp.route("/backup/<string:filename>", methods=["GET"])
@admin_required
@login_required
def get_backup_file(filename):
    """
    The page is used to get backup file and allow user to download it.
    """
    try:
        return send_file(str(backup_dir / filename), as_attachment=True)
    except FileNotFoundError:
        abort(404)
