from .database import db, Statuses, Items, Buildings, Admins, Users, Records, Revisions
from hashlib import sha256

def render_statuses():
    statuses = Statuses.query.all()
    return [status.description for status in statuses]

def render_items():
    items = Items.query.all()
    return [item.description for item in items]

def render_buildings():
    buildings = Buildings.query.all()
    return [building.description for building in buildings]

def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.password == sha256(password.encode('utf8').hexdigest()):
        return dict(id = Users.id, isAdmin=bool(Users.admin))
    else:
        return False
