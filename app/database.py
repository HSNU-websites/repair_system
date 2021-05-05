from typing import Sequence
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Statuses(db.Model):
    """
    Statuses.id = 1 will be default item
    """

    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None):
        if sequence is None:
            if s := db.session.query(db.func.max(Statuses.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description


class Items(db.Model):
    """
    Items.id = 1 will be default item
    """

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None):
        if sequence is None:
            if s := db.session.query(db.func.max(Items.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description


class Buildings(db.Model):
    """
    Buildings.id = 1 will be default building
    """

    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None):
        if sequence is None:
            if s := db.session.query(db.func.max(Buildings.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description


################################################################


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    # hashlib.sha256("pAs$W0rd".encode("utf-8")).hexdigest()
    password = db.Column(db.CHAR(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False)
    properties = db.Column(db.SmallInteger, server_default="0", nullable=False)
    email = db.Column(db.String(255), server_default="", nullable=False)
    flags = {
        "admin": 0x0001,
        "valid": 0x0002,
        "deleted": 0x0004,
    }
    __table_args__ = (
        db.Index(
            "idx_users_admin",
            db.text("((properties & {mask}))".format(mask=flags["admin"])),
        ),
    )

    def __init__(
        self, username, password, name, classnum, email=None, admin=False, valid=True
    ):
        self.username = username
        self.password = password
        self.name = name
        self.classnum = classnum
        self.email = email
        self.properties = 0
        self.isAdmin(admin)
        self.isValid(valid)

    def setFlag(self, flag: str, value: bool) -> bool:
        """
        In Linux file permission system, 1 is "executable", 2 is "writable", and 4 is "readable".
        Hence, 7 means the file is executable, writable and readable (7=1+2+4) to the user.
        Here, "admin" is similar to 1, "valid" similar to 2, and "deleted" similar to 4.
        And "properties" is similar to that 7, which indicates the combined status of the user in the database.
        Therefore, the properties can be changed by using Bitwise operator.
        """
        if flag not in Users.flags:
            return False
        if value:
            self.properties = self.properties | Users.flags[flag]
        else:
            self.properties = self.properties & (~Users.flags[flag])
        db.session.commit()
        return True

    def readFlag(self, flag: str) -> bool:
        return bool(self.properties & (Users.flags[flag]))

    def isAdmin(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag("admin")
        else:
            return self.setFlag("admin", value)

    def isValid(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag("valid")
        else:
            return self.setFlag("valid", value)

    def isMarkDeleted(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag("deleted")
        else:
            return self.setFlag("deleted", value)


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
