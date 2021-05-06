from hashlib import sha256
from os import urandom
from base64 import b64encode, b64decode

from passlib.context import CryptContext

from .database import (Buildings, Items, Records, Revisions, Statuses,
                       Unfinished, Users, db)

passwd_context = CryptContext(  # First scheme will be default
    schemes=["pbkdf2_sha256", "sha512_crypt"],
    deprecated="auto"
)


def render_statuses():
    statuses = db.session.query(
        Statuses.description).order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = db.session.query(Items.description).order_by(Items.sequence).all()
    return [item.description for item in items]


def render_buildings():
    buildings = (
        db.session.query(Buildings.description).order_by(
            Buildings.sequence).all()
    )
    return [building.description for building in buildings]


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

    # verify_and_update() returns tuple (verified: bool, new_hash: str|None)
    if user and (t := passwd_context.verify_and_update(password, user.password))[0]:
        if t[1]:
            user.password = t[1]
            db.session.commit()
        return dict(id=user.id, isAdmin=user.isAdmin())
    else:
        return False


def updateUnfinished():
    finishedStatus_id = 2
    Unfinished.__table__.drop(db.session)
    Unfinished.__table__.create(db.session)
    l = []
    for record in Records.query.all():
        if not (record.revisions and record.revisions[-1].status_id == finishedStatus_id):
            l += Unfinished(record.id)
    db.session.bulk_save_objects(l)
    db.session.commit()

def generateVerificationCode(user_id:int)->str:
    return b64encode(urandom(32))
