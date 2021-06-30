import datetime
import re  # regex
from pathlib import Path

import ujson

from .Archive import Archive
from .db_helper import updateUnfinisheds
from .model import *
from .common import cache

defaultTables = idTables
partition = 10000

backup_dir = Path("backup").resolve()  # absolute path to backup directory

# mail [].sort(key = lambda s: s[2])
# archiveName -> *.tar.gz / * (a folder)
# filename    -> *.json
# tables      -> [Users]
# tablenames  -> ["users"]

pattern = re.compile(r"^(?P<tableName>[a-z]+)_\d+.json$")


def convertTablename(filename: str):
    """
    'users_1.json' -> 'users'
    """
    if m := pattern.match(filename):
        return m.group("tableName")


def db_reprTest():
    """
    Test if repr(eval(obj)) == obj for tables
    that have at least one row.
    """
    b = True
    for t in defaultTables:
        if obj1 := t.query.first():
            obj2 = eval(repr(obj1))
            d1 = get_dict(obj1)
            d2 = get_dict(obj2)
            r = d1 == d2
            print(t.__tablename__, r)
            b = b and r
        else:
            print(t.__tablename__, "no item!!")
            b = False
    return b


def get_backups(reverse: bool = True) -> list:
    result = [a.name for a in backup_dir.glob("*.tar.xz")]
    result.sort(reverse=reverse)
    return result


def backup(tablenames: list[str] = None):
    archiveName = "Backup_{time}.tar.xz".format(
        time=datetime.datetime.now().strftime(filetimeformat))

    if tablenames is None:
        tablenames = topological_order
    else:
        tablenames = to_topological(tablenames, topological_order)
        if not validate_topological(tablenames, dependencyGraph):
            print("tablenames does not fulfill dependencies.")
            return False
    tables = [t for tn in tablenames if (t := tablenameRev[tn]) in idTables]

    archive = Archive(backup_dir / archiveName, "w")
    for t in tables:
        p = t.query.paginate(per_page=partition)
        while p.items:
            filename = "{tablename}_{count}.json".format(
                tablename=t.__tablename__, count=p.page)
            final = {
                "tablename": t.__tablename__,
                "data": [get_dict(row) for row in p.items]
            }
            archive.write(filename, final)
            p = p.next()
    print("Backup finished, file: {}".format(archiveName))

def restore(archiveName: str, tablenames: list[str] = None):
    # prepare tablelist
    archive = Archive(backup_dir / archiveName, "r")
    tablelist = dict()
    for fn in archive.getFileNames():
        tn = convertTablename(fn)
        if tn:
            l = tablelist.setdefault(tn, [])
            l.append(fn)
    for l in tablelist.values():  # sort filenames
        l.sort()
    tl = ujson.dumps(tablelist, ensure_ascii=False, escape_forward_slashes=False, sort_keys=True, indent=4)
    print("Archive {} has {}".format(archiveName, tl))

    # check if tablenames valid
    if tablenames is None:
        tablenames = list(tablelist.keys())
    else:
        temp = []
        for tn in tablenames:
            if tn in tablelist:
                temp.append(tn)
            else:
                print("table '{}' not in backup '{}'".format(tn, archiveName))
                return False
        tablenames = temp
    tablenames = to_topological(tablenames, topological_order)
    if not validate_topological(tablenames, dependencyGraph):
        print("tablenames does not fulfill dependencies.")
        return False

    # delete tables
    if "records" in tablenames or "revisions" in tablenames:
        Unfinisheds.query.delete()

    for tablename in reversed(tablenames):
        t = tablenameRev[tablename]
        t.query.delete()

    # restore tables
    for tablename in tablenames:
        t = tablenameRev[tablename]
        for filename in tablelist[tablename]:
            l = archive.read(filename)["data"]
            rows = [t(**d) for d in l]
            db.session.bulk_save_objects(rows)

    db.session.commit()
    cache.clear()
    updateUnfinisheds()


def del_backup(archiveName):
    a = backup_dir / archiveName
    if a.is_file():
        a.unlink()
