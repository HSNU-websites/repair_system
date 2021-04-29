from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Statuses(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description


class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description


class Buildings(db.Model):
    __tablename__ = 'buildings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description

################################################################


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True,
                         nullable=False, index=True)
    # hashlib.sha256(string.encoding("utf-8")).hexdigest()
    password = db.Column(db.CHAR(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, name, classnum):
        self.username = username
        self.password = password
        self.name = name
        self.classnum = classnum


class Admins(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True,
                         nullable=False, index=True)
    password = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey(
        'buildings.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'statuses.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False,
                     index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, type_id, building_id, location, status_id, time, description):
        self.user_id = user_id
        self.type_id = type_id
        self.building_id = building_id
        self.location = location
        self.status_id = status_id
        self.time = time
        self.description = description


class Revisions(db.Model):
    __tablename__ = 'revisions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.Integer, db.ForeignKey(
        'records.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admins.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'statuses.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, admin_id, status_id, time, description):
        self.record_id = record_id
        self.admin_id = admin_id
        self.status_id = status_id
        self.time = time
        self.description = description
