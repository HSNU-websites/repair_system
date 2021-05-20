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
    get_dict,
)


class User(UserMixin):
    pass


def render_statuses():
    statuses = Statuses.query.order_by(Statuses.sequence).all()
    return [status.description for status in statuses]


def render_items():
    items = Items.query.order_by(Items.sequence).all()
    return [(item.id, item.description) for item in items]


def render_buildings():
    buildings = Buildings.query.order_by(Buildings.sequence).all()
    return [(building.id, building.description) for building in buildings]


def render_system_setting():
    buildings = map(get_dict, Buildings.query.order_by(Buildings.sequence).all())
    items = map(get_dict, Items.query.order_by(Items.sequence).all())
    offices = map(get_dict, Offices.query.order_by(Offices.sequence).all())
    statuses = map(get_dict, Statuses.query.order_by(Statuses.sequence).all())
    return (buildings, items, offices, statuses)


def get_admin_emails():
    admins = db.session.query(Users.email).filter(Users.is_admin).all()
    return [admin.email for admin in admins]


def login_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.verify(password) and user.is_valid:
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.is_admin = user.is_admin
        return sessionUser
    else:
        return None


def load_user(user_id: str):
    # whether user_id is str or int doesn't matter
    user = Users.query.filter_by(id=user_id).first()
    if user and user.is_valid:
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.is_admin = user.is_admin
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
            l.append({"record_id": record.id})
    db.session.bulk_insert_mappings(Unfinisheds, l)
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
    item = db.session.query(Items.description).filter_by(id=record.item_id).scalar()
    building = db.session.query(Buildings.description).filter_by(id=record.building_id).scalar()
    l = []
    for rev in Revisions.query.filter_by(record_id=record.id).all():
        status = db.session.query(Statuses.description).filter_by(id=rev.status_id).scalar()
        l.append({
            "id": rev.id,
            "user": get_user(rev.user_id),
            "status": status,
            "insert_time": rev.insert_time.strftime(timeformat),
            "description": rev.description
        })

    return {
        "id": record.id,
        "user": get_user(record.user_id),
        "item": item,
        "building": building,
        "location": record.location,
        "insert_time": record.insert_time.strftime(timeformat),
        "update_time": record.update_time.strftime(timeformat),
        "description": record.description,
        "revisions": l
    }


def render_records(Filter=dict(), page=1, per_page=100) -> dict:
    q = Records.query
    valid = True
    if "username" in Filter:
        user_id = db.session.query(Users.id).filter_by(username=Filter.pop("username")).scalar()
        if valid := valid and user_id is not None:
            q = q.filter_by(user_id=user_id)

    if valid and "classnum" in Filter:
        unfin_query = db.session.query(Users.id).filter_by(classnum=Filter.pop("classnum"))
        if valid := valid and unfin_query.count() > 0:
            q = q.filter(Records.user_id.in_(unfin_query))

    if valid:
        Filter = {
            key: value
            for key, value in Filter.items()
            if key in Records.__mapper__.columns
        }
        q = q.filter_by(**Filter)

    if valid:
        l = [
            record_to_dict(record)
            for record in q.order_by(Records.update_time.desc()).offset((page - 1) * per_page).limit(per_page).all()
        ]
    else:
        l = []

    return {
        "page": page,
        "pages": ceil(q.count() / per_page) if valid else 0,
        "records": l
    }


def render_users(Filter=dict(), page=1, per_page=100) -> dict:
    q = db.session.query(
        Users.username, Users.name, Users.classnum, Users.email
    )
    Filter = {
        key: value
        for key, value in Filter.items()
        if key in Users.__mapper__.columns
    }
    q = q.filter_by(**Filter)
    l = []
    for user in q.offset((page - 1) * per_page).limit(per_page).all():
        l.append({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "classnum": user.classnum,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_valid": user.is_valid,
            "is_mark_deleted": user.is_mark_deleted,
        })
    return {
        "page": page,
        "pages": ceil(q.count() / per_page),
        "users": l
    }


def insert(tablename: str, data: dict):
    """
    Statuses, Offices, Items, Buildings only
    """
    try:
        if (t := tablenameRev[tablename]) not in sequenceTables:
            return False
        db.session.add(t(**data))
        db.session.commit()
        updateSequence([t])
        return True
    except:
        return False


def update(tablename: str, data: dict):
    """
    Statuses, Offices, Items, Buildings only
    """
    try:
        if (t := tablenameRev[tablename]) not in sequenceTables:
            return False
        id = data.pop("id")
        t.query.filter_by(id=id).update(data)
        db.session.commit()
        return True
    except:
        return False


def delete(tablename: str, id: int):
    """
    Statuses, Offices, Items, Buildings only
    """
    try:
        if (t := tablenameRev[tablename]) not in sequenceTables:
            return False
        t.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except:
        return False
    # todo fix foreign key constraint


def add_users(data: list[dict]):
    """
    returns a list of username that already exist
    """
    l = []
    already_exist = []
    for d in data:
        if "username" in d:
            if Users.username_exists(d["username"]):
                already_exist.append(d["username"])
            else:
                l.append(Users.new(**d))
    db.session.bulk_save_objects(l)
    db.session.commit()
    return already_exist


def update_users(data: list[dict]):
    l = []
    for d in data:
        if "password" in d:
            d["password_hash"] = Users.passwd_hash(d.pop("password"))
        d = {
            key: value
            for key, value in d.items()
            if key in Users.__mapper__.columns
        }
        if len(d) >= 2 and "id" in d:
            l.append(d)
    db.session.bulk_update_mappings(Users, l)
    db.session.commit()


def del_users(ids: list[int], force=False):
    """
    no force: mark users as deleted if user_id in records or revisions
    force: update records and revisions set user_id = 1 (deleted)
           and delete user
    """
    s = set()
    if force:
        for user_id in ids:
            Records.query.filter_by(user_id=user_id).update({"user_id": 1})
            Revisions.query.filter_by(user_id=user_id).update({"user_id": 1})
            s.add(user_id)
    else:
        for user_id in ids:
            a = db.session.query(db.exists().where(
                Records.user_id == user_id)).scalar()
            b = db.session.query(db.exists().where(
                Revisions.user_id == user_id)).scalar()
            if a or b:
                u = Users.query.filter_by(id=user_id).first()
                u.is_valid = False
                u.is_mark_deleted = True
            else:
                s.add(user_id)
    if s:
        Users.query.filter(Users.id.in_(s)).delete()
        db.session.commit()
