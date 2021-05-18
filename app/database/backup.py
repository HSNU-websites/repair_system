import datetime
import re  # regex
from pathlib import Path

from .model import *
from .Archive import Archive
from .db_helper import updateUnfinisheds

defaultTables = idTables
partition = 1000

backup_dir = Path("Backup")

# mail [].sort(key = lambda s: s[2])
# archiveName -> *.tar.gz / * (a folder)
# filename    -> *.json
# tables      -> [Users]
# tablenames  -> ["users"]

pattern = re.compile(r"^(?P<tableName>[a-z]+)(_\d+)?.json$")


def convertTablename(filename: str):
    """
    'buildings.json'    -> 'buildings'
    'users_1-1000.json' -> 'users'
    """
    if m := pattern.match(filename):
        return m.group("tableName")


def get_dict(row):
    """
    Get pure dict from table without relationship.
    datetime.datetime will be converted to str
    """
    def process_value(value):
        if isinstance(value, datetime.datetime):
            return value.strftime(timeformat)
        else:
            return value
    return {
        key: process_value(row.__dict__[key])
        for key in type(row).__mapper__.columns.keys()
    }


def db_reprTest():
    """
    Test if repr(eval(obj)) == obj for tables
    that have at least one row.
    """
    b = True
    for t in defaultTables:
        obj1 = t.query.first()
        obj2 = eval(repr(obj1))
        d1 = get_dict(obj1)
        d2 = get_dict(obj2)
        r = d1 == d2
        print(t.__tablename__, r)
        b = b and r
    return b


def getBackups() -> list:
    return list(backup_dir.iterdir())


def set_diff(a: set, b: set, modify=False) -> list[set]:
    """
    if modify=True, set 'a' and 'b' will be modified,
    but it's faster since it doesn't need copy.
    returns list[set(only in a), set(in a and b), set(only in b)]
    """
    if not modify:
        a = a.copy()
        b = b.copy()
    result = [set(), set(), set()]
    for value in a:
        if value in b:
            result[1].add(value)
            b.remove(value)
        else:
            result[0].add(value)
    result[2] = b
    return result


def backup(tables: list[db.Model] = None):  # path not fix
    archiveName = "Backup_{time}.tar.xz".format(
        time=datetime.datetime.now().strftime(timeformat))
    if tables is None:
        tables = defaultTables
    else:
        tables = filter(lambda x: x in idTables, tables)

    archive = Archive(backup_dir/archiveName, "w")
    for t in tables:
        # max = t.query.count()
        # if max <= partition:
        filename = "{tablename}.json".format(tablename=t.__tablename__)
        final = dict()
        final[t.__tablename__] = [repr(row) for row in t.query.all()]
        archive.write(filename, final)
        # else:
        #     p = t.query.paginate(per_page=partition)
        #     while p.items:
        #         filename = "{tablename}_{count}.json".format(
        #             tablename=t.__tablename__, count=p.page)
        #         final = dict()
        #         final[t.__tablename__] = [
        #             repr(row) for row in p.items
        #         ]
        #         archive.write(filename, final)
        #         p = p.next()
    print("Backup finished, file: {}".format(archiveName))


def restore(archiveName: str, tables: list = None, insert=True, update=True, delete=True):
    Unfinisheds.query.delete()
    if tables is None:
        tables = defaultTables
    tablenames = [t.__tablename__ for t in tables]
    print("Restoring tables {}".format(tablenames))
    archive = Archive(backup_dir/archiveName, "r")
    print("Archive {} has {}".format(archiveName, archive.getFileNames()))
    for filename in archive.getFileNames():
        tablename = convertTablename(filename)
        if tablename in tablenames:
            print("Restoring {}".format(tablename))
            t = tablenameRev[tablename]
            l = archive.read(filename)[tablename]
            temp = [get_dict(eval(obj)) for obj in l]
            rows = {d["id"]: d for d in temp}
            a = set(rows.keys())
            b = {row.id for row in db.session.query(t.id).all()}
            result = set_diff(a, b, modify=True)
            if insert:
                print("Inserting {}".format(sorted(result[0])))
                ld = [rows[id] for id in result[0]]
                db.session.bulk_insert_mappings(t, ld)
            if update:
                print("Updating {}".format(sorted(result[1])))
                ld = [rows[id] for id in result[1]]
                db.session.bulk_update_mappings(t, ld)
            if delete:
                print("Deleting {}".format(sorted(result[2])))
                t.query.filter(t.id.in_(result[2])).delete()
    db.session.commit()
    updateUnfinisheds()
