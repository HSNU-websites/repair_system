from flask_login import login_required
from . import admin_bp

@admin_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_page():
    pass

@admin_bp.route("/system", methods=["GET", "POST"])
@login_required
def system_page():
    pass