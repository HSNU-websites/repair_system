from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

db = SQLAlchemy()
timeformat = r"%Y-%m-%dT%H:%M:%S"
dateformat = r"%Y-%m-%d"
filetimeformat = r"%Y-%m-%dT%H-%M-%S"
timeformat_re_str = r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}"
finishedStatus_id = 2

passwd_context = CryptContext(  # First scheme will be default
    schemes=["pbkdf2_sha256", "sha512_crypt"], deprecated="auto"
)


def get_dict(row):
    """
    Get pure dict from table without relationship.
    datetime.datetime will be converted to str
    """
    import datetime

    def process_value(value):
        if isinstance(value, datetime.datetime):
            return value.strftime(timeformat)
        else:
            return value

    if type(row) not in allTables:
        return {}
    else:
        return {
            key: process_value(row.__dict__[key])
            for key in type(row).__mapper__.columns.keys()
        }
