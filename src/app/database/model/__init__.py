from .common import (
    dateformat,
    db,
    filetimeformat,
    finishedStatus_id,
    timeformat,
    get_dict,
    get_foreign_key_dependencies,
    topological_sort,
    to_topological,
    validate_topological
)
from .Buildings import Buildings
from .Items import Items
from .Offices import Offices
from .Records import Records
from .Revisions import Revisions
from .Statuses import Statuses
from .Unfinisheds import Unfinisheds
from .Users import Users

allTables = {Buildings, Items, Records, Revisions, Statuses, Users, Unfinisheds, Offices}
tablenameRev = {t.__tablename__: t for t in allTables}
idTables = {t for t in allTables if "id" in t.__mapper__.columns}
sequenceTables = {t for t in allTables if "sequence" in t.__mapper__.columns}
dependencyGraph =  {
    t.__tablename__: get_foreign_key_dependencies(t)
    for t in idTables
}
topological_order = topological_sort(dependencyGraph)

# __all__ = []



