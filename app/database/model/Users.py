from .common import db, passwd_context


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    # passwd_context.hash("pAs$W0rd")
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    classnum = db.Column(db.Integer, nullable=False)
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

    def __init__(
        self,
        username,
        password_hash,
        name,
        classnum,
        email="",
        admin=False,
        valid=True,
        **kwargs
    ):
        self.username = username
        self.password_hash = password_hash
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
        return "Users(id={id},username='{username}',password_hash='{password_hash}',name='{name}',classnum={classnum},email='{email}',properties={properties})".format(
            **self.__dict__
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
        db.session.commit()

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

    def verify(self, password: str) -> bool:
        result, new_hash = passwd_context.verify_and_update(
            password, self.password_hash
        )
        if new_hash:
            self.password_hash = new_hash
            db.session.commit()
        return result
