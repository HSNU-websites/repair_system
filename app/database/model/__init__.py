from .common import db, timeformat, filetimeformat
from .Buildings import Buildings
from .Items import Items
from .Records import Records
from .Revisions import Revisions
from .Statuses import Statuses
from .Unfinisheds import Unfinisheds
from .Users import Users
from .Offices import Offices

allTables = {Buildings, Items, Records, Revisions, Statuses, Users,  Unfinisheds, Offices}
tablenameRev = {t.__tablename__: t for t in allTables}
idTables = {t for t in allTables if "id" in t.__mapper__.columns}
sequenceTables = {t for t in allTables if "sequence" in t.__mapper__.columns}

# __all__ = []
