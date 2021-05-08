from .common import db, timeformat
from .Buildings import Buildings
from .Items import Items
from .Records import Records
from .Revisions import Revisions
from .Statuses import Statuses
from .Unfinished import Unfinished
from .Users import Users

tables = {Statuses, Items, Buildings, Users, Records, Revisions, Unfinished}
idTables = {t for t in tables if "id" in t.__dict__}
sequenceTables = {t for t in tables if "sequence" in t.__dict__}

# __all__ = []
