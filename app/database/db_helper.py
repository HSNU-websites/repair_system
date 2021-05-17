from base64 import b64decode, b64encode
from hashlib import sha256
from math import ceil
from os import urandom

from flask_login import UserMixin

from .model import (
    Buildings,
    Items,
    Records,
    Revisions,
    Statuses,
    Unfinisheds,
    Users,
    Offices,
    db,
    sequenceTables,
    tablenameRev,
    timeformat,
)


class User(UserMixin):
    pass


def render_statuses():
    statuses = db.session.query(
        Statuses.description).order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = db.session.query(
        Items.id, Items.description).order_by(Items.sequence).all()
    return [(item.id, item.description) for item in items]


def render_buildings():
    buildings = (
        db.session.query(Buildings.id, Buildings.description)
        .order_by(Buildings.sequence)
        .all()
    )
    return [(building.id, building.description) for building in buildings]


def render_system_setting():
    buildings = db.session.query(Buildings).order_by(Buildings.sequence).all()
    items = db.session.query(Items).order_by(Items.sequence).all()
    offices = db.session.query(Offices).order_by(Offices.sequence).all()
    statuses = db.session.query(Statuses).order_by(Statuses.sequence).all()
    return (buildings, items, offices, statuses)


def get_admin_emails():
    admins = (
        # only "(properties & :mask) > 0" works with index
        db.session.query(Users.email)
        .from_statement(
            db.text("SELECT users.email FROM users WHERE (properties & :mask) > 0")
        )
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


def updateUnfinisheds():
    finishedStatus_id = 2
    Unfinisheds.query.delete()
    l = []
    for record in Records.query.all():
        r = (
            db.session.query(Revisions.status_id)
            .filter_by(record_id=record.id)
            .order_by(Revisions.id.desc()).first()
        )
        if not (r and r.status_id == finishedStatus_id):
            l.append(Unfinisheds(record_id=record.id))
    db.session.bulk_save_objects(l)
    db.session.commit()


def updateSequence(tables=None):
    """
    table: a list of sequence tables
    assign rows where sequence=0
    """
    if tables is None:
        tables = sequenceTables
    else:
        tables = filter(lambda x: x in sequenceTables, tables)

    for table in tables:
        if r := db.session.query(db.func.max(table.sequence)).first():
            max = r[0]
        else:
            max = 0
        l = []
        for row in table.query.filter_by(sequence=0).order_by(table.id).all():
            row.sequence = (max := max + 1)
            l.append(row)
        db.session.bulk_save_objects(l)
    db.session.commit()


def generateVerificationCode(user_id: int) -> str:
    return b64encode(urandom(32))


def add_record(user_id, building_id, location, item_id, description):
    db.session.add(
        Records(user_id, item_id, building_id, location, description)
    )
    db.session.commit()


def get_user(user_id) -> dict:
    user = db.session.query(
        Users.username, Users.name, Users.classnum
    ).filter_by(id=user_id).first()
    return {
        "username": user.username,
        "name": user.name,
        "classnum": user.classnum
    }

def record_to_dict(record):
    item = db.session.query(Items.description).filter_by(
        id=record.item_id).first()[0]
    building = db.session.query(Buildings.description).filter_by(
        id=record.building_id).first()[0]
    insert_time = record.insert_time.strftime(timeformat)
    update_time = record.update_time.strftime(timeformat)
    l = []
    for rev in Revisions.query.filter_by(record_id=record.id).all():
        status = db.session.query(Statuses.description).filter_by(
            id=rev.status_id).first()[0]
        time = rev.insert_time.strftime(timeformat)
        l.append({
            "user": get_user(rev.user_id),
            "status": status,
            "insert_time": time,
            "description": rev.description
        })

    return {
        "user": get_user(record.user_id),
        "item": item,
        "building": building,
        "location": record.location,
        "insert_time": insert_time,
        "update_time": update_time,
        "description": record.description,
        "revisions": l
    }


def render_user_records(user_id) -> list:
    l = []
    for record in Records.query.filter_by(user_id=user_id).order_by(Records.update_time.desc()).all():
        l.append(record_to_dict(record))
    return l


def render_all_records(filter: dict = None, page=1, per_page=100) -> dict:
    if filter is None:
        q = Records.query
    else:
        if "username" in filter:
            u = db.session.query(Users.id).filter_by(username=filter.pop("username"))
            if u:
                q = q.filter_by(user_id=u.id)
        if "classnum" in filter:
            u = db.session.query(Users.id).filter_by(username=filter.pop("classnum"))
            if u:
                q = q.filter_by(user_id=u.id)
        q = q.filter_by(**filter)

    l = []
    for record in q.order_by(Records.update_time.desc()).offset((page-1)*per_page).limit(per_page).all():
        l.append(record_to_dict(record))

    return {
        "page": page,
        "pages": ceil(Records.query.count()/per_page),
        "records": l
    }


def insert(tablename: str, data: dict):
    try:
        t = tablenameRev[tablename]
        db.session.add(t(**data))
        db.session.commit()
        updateSequence([t])
        return True
    except:
        return False


def update(tablename: str, data: dict):
    try:
        t = tablenameRev[tablename]
        id = data.pop("id")
        t.query.filter_by(id=id).update(data)
        db.session.commit()
        return True
    except:
        return False


def delete(tablename: str, id: int):
    try:
        t = tablenameRev[tablename]
        t.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except:
        return False
    # todo fix foreign key constraint
