from .database import db, Statuses, Items, Buildings, Users, Records, Revisions, Unfinished
from hashlib import sha256
from passlib.context import CryptContext
# pbkdf2_sha256
# verify_and_update

passwd_context = CryptContext( # First scheme will be default
    schemes=["pbkdf2_sha256", "sha512_crypt"],
    deprecated="auto"
)

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
        .params(mask=Users.flags.admin)
        .all()
    )
    return [admin.email for admin in admins]

# need revision
def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and (t:=passwd_context.verify_and_update(password, user.password))[0]:
        # verify_and_update() return (True|false, str|None)    
        if t[1] is not None:
            user.password = t[1]
            db.session.commit()
        return dict(id=user.id, isAdmin=user.isAdmin())
    else:
        return False

# not finished
def updateUnfinished():
    finished =1000 ####
    Unfinished.__table__.drop(db.session)
    for record in Records.query.all():
        if record and record.revisions and record.revisions[-1].id == finished:
           pass
