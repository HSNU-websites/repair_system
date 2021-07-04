from .common import db, passwd_context
from sqlalchemy.ext.hybrid import hybrid_property


class Users(db.Model):
    """
    The table stores all users.

    id: PK, and it is used as user.id in flask_login system.
    username: User's student id, and admins have a nickname.
    password_hash: Hashed password.
    name: User's real name.
    classnum: User's class number, and 0 will be the value if the user is an admin.
    properties: See `setFlag` doc.
    email: User's email, and students will have empty string since their email can be inferred from their student id.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    # passwd_context.hash("pAs$W0rd")
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False, index=True)
    properties = db.Column(db.SmallInteger, nullable=False)
    email = db.Column(db.String(255), nullable=False)

    class flags:
        admin = 0x0001
        valid = 0x0002
        deleted = 0x0004

    __table_args__ = (
        db.Index(
            "idx_users_admin",
            db.text("((properties & {mask}))".format(mask=flags.admin)),
        ),
    )

    def setFlag(self, flag: int, value: bool):
        """
        In Linux file permission system, 1 is "executable", 2 is "writable", and 4 is "readable".
        Hence, 7 means the file is executable, writable and readable (7=1+2+4) to the user.
        Here, "admin" is similar to 1, "valid" similar to 2, and "deleted" similar to 4.
        And "properties" is similar to that 7, which indicates the combined status of the user in the database.
        Therefore, the properties can be changed by using Bitwise operator.
        """
        if value:
            self.properties = self.properties | flag
        else:
            self.properties = self.properties & (~flag)

    def readFlag(self, flag: int) -> bool:
        return bool(self.properties & flag)

    # hybrid_property for is_admin
    @hybrid_property
    def is_admin(self):
        return self.readFlag(Users.flags.admin)

    @is_admin.setter
    def is_admin(self, value):
        self.setFlag(Users.flags.admin, value)

    @is_admin.expression
    def is_admin(self):
        """
        SQL query expression that works with 'idx_users_admin'

        """
        return self.properties.op("&")(Users.flags.admin) == Users.flags.admin

    # hybrid_property for is_valid
    @hybrid_property
    def is_valid(self):
        return self.readFlag(Users.flags.valid)

    @is_valid.setter
    def is_valid(self, value):
        self.setFlag(Users.flags.valid, value)

    @is_valid.expression
    def is_valid(self):
        return self.properties.op("&")(Users.flags.valid) == Users.flags.valid

    # hybrid_property for is_marked_deleted
    @hybrid_property
    def is_marked_deleted(self):
        return self.readFlag(Users.flags.deleted)

    @is_marked_deleted.setter
    def is_marked_deleted(self, value):
        self.setFlag(Users.flags.deleted, value)

    @is_marked_deleted.expression
    def is_marked_deleted(self):
        return self.properties.op("&")(Users.flags.deleted) == Users.flags.deleted

    def __init__(self, id, username, password_hash, name, classnum, properties, email):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.classnum = classnum
        self.properties = properties
        self.email = email

    def __repr__(self):
        return (
            "Users(id={id},username='{username}',password_hash='{password_hash}',name='{name}',classnum={classnum},properties={properties},email='{email}')"
            .format(**self.__dict__)
        )

    def verify(self, password: str) -> bool:
        result, new_hash = passwd_context.verify_and_update(
            password, self.password_hash
        )
        if new_hash:
            self.password_hash = new_hash
            db.session.commit()
        return result

    @classmethod
    def username_exists(cls, username):
        return db.session.query(db.exists().where(cls.username == username)).scalar()

    @classmethod
    def new(cls, username, password="", name="", classnum=0, email="", is_admin=False, is_valid=True, is_marked_deleted=False):
        u = cls(
            id=None,
            username=username[:16],
            password_hash=passwd_context.hash(password) if password else "",
            name=name[:255],
            classnum=classnum,
            properties=0,
            email=email[:255]
        )
        u.is_admin = is_admin
        u.is_valid = is_valid
        u.is_marked_deleted = is_marked_deleted
        return u

    def update(self, password=None, name=None, classnum=None, email=None, is_admin=None, is_valid=None, is_marked_deleted=None):
        if password is not None:
            self.password_hash = passwd_context.hash(password) if password else ""
        if name is not None:
            self.name = name[:255]
        if classnum is not None:
            self.classnum = classnum
        if email is not None:
            self.email = email[:255]
        if is_admin is not None:
            self.is_admin = is_admin
        if is_valid is not None:
            self.is_valid = is_valid
        if is_marked_deleted is not None:
            self.is_marked_deleted = is_marked_deleted
