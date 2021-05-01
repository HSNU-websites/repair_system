from . import user_bp
from app import user

@user_bp.route("/report")
def report_page():
    pass

@user_bp.route("/dashboard")
def dashboard_page():
    pass