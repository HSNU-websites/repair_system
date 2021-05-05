from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
timeformat = "%Y-%m-%dT%H-%M-%S"


class Statuses(db.Model):
    """
    Statuses.id = 1 will be default item
    """
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Statuses.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Statuses(id={id}, sequence={sequence}, description='{description}')".format(**self.__dict__)


class Items(db.Model):
    """
    Items.id = 1 will be default item
    """
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Items.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
            # flush
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Items(id={id},sequence={sequence},description='{description}')".format(**self.__dict__)


class Buildings(db.Model):
    """
    Buildings.id = 1 will be default building
    """
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Buildings.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Buildings(id={id},sequence={sequence},description='{description}')".format(**self.__dict__)


################################################################

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    # hashlib.sha256("pAs$W0rd".encode("utf-8")).hexdigest()
    password = db.Column(db.CHAR(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False)
    properties = db.Column(db.SmallInteger, nullable=False)
    email = db.Column(db.String(255), nullable=False)

    class flags():
        admin = 0x0001
        valid = 0x0002
        deleted = 0x0004

    __table_args__ = (
        db.Index("idx_users_admin",
                 db.text("((properties & {mask}))".format(mask=flags.admin))),
    )

    def __init__(self, username, password, name, classnum, email="", admin=False, valid=True, **kwargs):
        self.username = username
        self.password = password
        self.name = name
        self.classnum = classnum
        self.email = email
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "properties" in kwargs:
            self.properties = kwargs["properties"]
        else:
            self.properties = 0
            self.isAdmin(admin)
            self.isValid(valid)

    def __repr__(self):
        return "Users(id={id},username='{username}',password='{password}',name='{name}',classnum={classnum},email='{email}',properties={properties})".format(**self.__dict__)

    def setFlag(self, flag: int, value: bool) -> bool:
        if value:
            self.properties = self.properties | flag
        else:
            self.properties = self.properties & (~flag)
        db.session.commit()
        return True

    def readFlag(self, flag: int) -> bool:
        return bool(self.properties & flag)

    def isAdmin(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag(Users.flags.admin)
        else:
            return self.setFlag(Users.flags.admin, value)

    def isValid(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag(Users.flags.valid)
        else:
            return self.setFlag(Users.flags.valid, value)

    def isMarkDeleted(self, value: bool = None) -> bool:
        if value is None:
            return self.readFlag(Users.flags.deleted)
        else:
            return self.setFlag(Users.flags.deleted, value)


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.ForeignKey("items.id"), nullable=False)
    building_id = db.Column(db.ForeignKey("buildings.id"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(db.TIMESTAMP,
                     server_default=db.func.now(),
                     nullable=False,
                     index=True)
    description = db.Column(db.String(255), nullable=False)
    revisions = db.relationship("Revisions")

    def __init__(self, user_id, item_id, building_id, location, description, **kwargs):
        self.user_id = user_id
        self.item_id = item_id
        self.building_id = building_id
        self.location = location
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "time" in kwargs:
            self.time = datetime.datetime.strptime(kwargs["time"], timeformat)

    def __repr__(self):
        return "Records(id={id},user_id={user_id},item_id={item_id},building_id={building_id},location='{location}',time='{mytime}',description='{description}')".format(mytime=self.time.strftime(timeformat), **self.__dict__)


class Revisions(db.Model):
    __tablename__ = "revisions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.ForeignKey("records.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    status_id = db.Column(db.ForeignKey("statuses.id"), nullable=False)
    time = db.Column(db.TIMESTAMP,
                     server_default=db.func.now(),
                     nullable=False,
                     index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, user_id, status_id, description, **kwargs):
        self.record_id = record_id
        self.user_id = user_id
        self.status_id = status_id
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "time" in kwargs:
            self.time = datetime.datetime.strptime(kwargs["time"], timeformat)

    def __repr__(self):
        return "Revisions(id={id},record_id={record_id},user_id={user_id},status_id={status_id},time='{mytime}',description='{description}')".format(mytime=self.time.strftime(timeformat), **self.__dict__)


class Unfinished(db.Model):
    """
    This TABLE is used to optimize query.
    Do not need to backup.
    """
    __tablename__ = "unfinisheds"
    record_id = db.Column(db.ForeignKey("records.id"), primary_key=True)
    record = db.relationship("Records")

    def __init__(self, record_id):
        self.record_id = record_id

    def __repr__(self):
        return "Unfinished(record_id={record_id})".format(**self.__dict__)

