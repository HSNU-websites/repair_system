# The routes are for students and admins as well.

from flask import Blueprint

user_bp = Blueprint("user", __name__)

from . import routes
