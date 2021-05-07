from base64 import b64decode, b64encode
from hashlib import sha256
from os import urandom

from flask_login import UserMixin

from .database import (
    Buildings,
    Items,
    Records,
    Revisions,
    Statuses,
    Unfinished,
    Users,
    db,
)


class User(UserMixin):
    pass


def render_statuses():
    statuses = db.session.query(Statuses.description).order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = db.session.query(Items).order_by(Items.sequence).all()
    return [(item.id, item.description) for item in items]


def render_buildings():
    buildings = (
        db.session.query(Buildings).order_by(Buildings.sequence).all()
    )
    return [(building.id, building.description) for building in buildings]


def get_admin_emails():
    admins = (
        db.session.query(Users.email)
        .from_statement(db.text("SELECT * FROM users WHERE (properties & :mask) > 0"))
        .params(mask=Users.flags.admin)
        .all()
    )
    return [admin.email for admin in admins]


# need revision


def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.verify(password) and user.isValid():
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.isAdmin = user.isAdmin()
        return sessionUser
    else:
        return False


def load_user(user_id: str):
    user = Users.query.filter_by(id=user_id).first()
    if user.isValid():
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.isAdmin = user.isAdmin()
        return sessionUser
    else:
        return None


def updateUnfinished():
    finishedStatus_id = 2
    Unfinished.__table__.drop(db.engine)
    Unfinished.__table__.create(db.engine)
    l = []
    for record in Records.query.all():
        if not (
            record.revisions and record.revisions[-1].status_id == finishedStatus_id
        ):
            l.append(Unfinished(record_id=record.id))
    db.session.bulk_save_objects(l)
    db.session.commit()


def generateVerificationCode(user_id: int) -> str:
    return b64encode(urandom(32))


def add_record(building_id, location, item_id, description):
    pass
