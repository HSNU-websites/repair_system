from app import user

from . import user_bp


@user_bp.route("/report")
def report_page():
    pass


@user_bp.route("/dashboard")
def dashboard_page():
    pass
