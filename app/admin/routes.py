from flask_login import login_required
from . import admin_bp
from ..users import admin_required

@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page():
    pass

@admin_bp.route("/system", methods=["GET", "POST"])
@admin_required
@login_required
def system_page():
    pass