from .common import db, timeformat, passwd_context
from .Buildings import Buildings
from .Items import Items
from .Records import Records
from .Revisions import Revisions
from .Statuses import Statuses
from .Unfinisheds import Unfinisheds
from .Users import Users
from .Offices import Offices

tables = {Statuses, Offices, Items, Buildings, Users, Records, Revisions, Unfinisheds}
tablenameRev = {t.__tablename__:t for t in tables}
idTables = {t for t in tables if "id" in t.__dict__}
sequenceTables = {t for t in tables if "sequence" in t.__dict__}

# __all__ = []
