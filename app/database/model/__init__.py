from .common import db, timeformat, filetimeformat
from .Buildings import Buildings
from .Items import Items
from .Records import Records
from .Revisions import Revisions
from .Statuses import Statuses
from .Unfinisheds import Unfinisheds
from .Users import Users
from .Offices import Offices

allTables = {Buildings, Items, Records, Revisions, Statuses, Users, Unfinisheds, Offices}
tablenameRev = {t.__tablename__: t for t in allTables}
idTables = {t for t in allTables if "id" in t.__mapper__.columns}
sequenceTables = {t for t in allTables if "sequence" in t.__mapper__.columns}

# __all__ = []


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
