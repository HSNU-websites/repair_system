from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Statuses(db.Model):
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description


# id = 1 will be default item


class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description


# id = 1 will be default building


class Buildings(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description


################################################################


class Admins(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), unique=True, nullable=False)
    email = db.Column(db.String(255), server_default="", nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False, index=True)
    # hashlib.sha256("pAs$W0rd".encode("utf-8")).hexdigest()
    password = db.Column(db.CHAR(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False)
    # bool(admin) to check if it is admin
    admin = db.relationship("Admins", uselist=False)

    def __init__(self, username, password, name, classnum):
        self.username = username
        self.password = password
        self.name = name
        self.classnum = classnum


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.ForeignKey("items.id"), nullable=False)
    building_id = db.Column(db.ForeignKey("buildings.id"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False, index=True
    )
    description = db.Column(db.String(255), nullable=False)
    revisions = db.relationship("Revisions")

    def __init__(self, user_id, item_id, building_id, location, description):
        self.user_id = user_id
        self.item_id = item_id
        self.building_id = building_id
        self.location = location
        self.description = description


class Revisions(db.Model):
    __tablename__ = "revisions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.ForeignKey("records.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    status_id = db.Column(db.ForeignKey("statuses.id"), nullable=False)
    time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False, index=True
    )
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, user_id, status_id, description):
        self.record_id = record_id
        self.user_id = user_id
        self.status_id = status_id
        self.description = description
