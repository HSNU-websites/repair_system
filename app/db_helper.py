from .database import db, Statuses, Items, Buildings, Users, Records, Revisions
from hashlib import sha256


def render_statuses():
    statuses = db.session.query(Statuses.description).order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = db.session.query(Items.description).order_by(Items.sequence).all()
    return [item.description for item in items]


def render_buildings():
    buildings = (
        db.session.query(Buildings.description).order_by(Buildings.sequence).all()
    )
    return [building.description for building in buildings]


def get_admin_emails():
    admins = (
        db.session.query(Users.email)
        .from_statement(db.text("SELECT * FROM users WHERE (properties & :mask) > 0"))
        .params(mask=Users.flags["admin"])
        .all()
    )
    return [admin.email for admin in admins]


def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.password == sha256(password.encode("utf8")).hexdigest():
        return dict(id=user.id, isAdmin=user.isAdmin())
    else:
        return False

def updateUnfinished():
    pass
