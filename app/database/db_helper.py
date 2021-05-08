from base64 import b64decode, b64encode
from hashlib import sha256
from os import urandom

from flask_login import UserMixin

from .model import (
    Buildings,
    Items,
    Records,
    Revisions,
    Statuses,
    Unfinished,
    Users,
    db,
    sequenceTables,
)


class User(UserMixin):
    pass


def render_statuses():
    statuses = db.session.query(
        Statuses.description).order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = db.session.query(Items).order_by(Items.sequence).all()
    return [(item.id, item.description) for item in items]


def render_buildings():
    buildings = (
        db.session.query(Buildings.description).order_by(
            Buildings.sequence).all()
    )
    return [(building.id, building.description) for building in buildings]


def get_admin_emails():
    admins = (
        # only "(properties & :mask) > 0" works with index
        db.session.query(Users.email)
        .from_statement(db.text("SELECT users.email FROM users WHERE (properties & :mask) > 0"))
        .params(mask=Users.flags.admin)
        .all()
    )
    return [admin.email for admin in admins]


def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.verify(password) and user.isValid():
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.isAdmin = user.isAdmin()
        return sessionUser
    else:
        return None


def load_user(user_id: str):
    # whether user_id is str or int doesn't matter
    user = Users.query.filter_by(id=user_id).first()
    if user and user.isValid():
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.isAdmin = user.isAdmin()
        return sessionUser
    else:
        return None


def updateUnfinished():
    finishedStatus_id = 2
    Unfinished.query.delete()
    l = []
    for record in Records.query.all():
        if not (
            record.revisions and record.revisions[-1].status_id == finishedStatus_id
        ):
            l.append(Unfinished(record_id=record.id))
    db.session.bulk_save_objects(l)
    db.session.commit()


def updateSequence(table: db.Model):
    """
    assign rows where sequence=0
    """
    if table not in sequenceTables:
        return False
    if r := db.session.query(db.func.max(table.sequence)).first():
        max = r[0]
    else:
        max = 0
    l = []
    for row in table.query.filter(table.sequence == 0).order_by(table.id).all():
        row.sequence = (max := max+1)
        l.append(row)
    db.session.bulk_save_objects(l)
    db.session.commit()
    return True


def generateVerificationCode(user_id: int) -> str:
    return b64encode(urandom(32))


def add_record(building_id, location, item_id, description):
    pass
