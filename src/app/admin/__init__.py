# The routes are all for admins.

from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from . import routes
from . import backend_routes
