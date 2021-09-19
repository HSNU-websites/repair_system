import datetime
import logging
import re  # regex
from pathlib import Path

import ujson

from ..myhandler import timeformat_to_regex
from .common import cache
from .db_helper import updateUnfinisheds
from .model import (
    Unfinisheds,
    db,
    dependencyGraph,
    filetimeformat,
    get_dict,
    idTables,
    tablenameRev,
    to_topological,
    topological_order,
    validate_topological
)
from .myarchive import Archive

defaultTables = idTables
partition = 10000

backup_dir = Path("backup").resolve()  # absolute path to backup directory
backup_logger = logging.getLogger("backup")
backup_name = "Backup_{time}.tar.xz".format(time=filetimeformat)
backup_auto_name = "Backup_{time}_auto.tar.xz".format(time=filetimeformat)
backup_auto_name_match = timeformat_to_regex(backup_auto_name)

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


def backup(tablenames: list[str] = None, scheduled: bool = False):
    try:
        if scheduled:
            archiveName = datetime.datetime.now().strftime(backup_auto_name)
        else:
            archiveName = datetime.datetime.now().strftime(backup_name)

        backup_logger.info("Starting backup...")
        backup_logger.info("tables: {}".format(tablenames))

        if tablenames is None:
            tablenames = topological_order
            backup_logger.info("use default tables: {}".format(tablenames))
        else:
            for tn in tablenames:
                if tn not in idTables:
                    raise RuntimeError("table '{}' not available".format(tn))
            tablenames = to_topological(tablenames, topological_order)
            if not validate_topological(tablenames, dependencyGraph):
                raise RuntimeError("tablenames does not fulfill dependencies")

        tables = [tablenameRev[tn] for tn in tablenames]

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
    except RuntimeError as e:
        backup_logger.error(e)
        backup_logger.error("Abort backup")
        raise e
    else:
        backup_logger.info("Backup finished, file: {}".format(archiveName))


def scheduled_backup(backupCount=60):
    backup(scheduled=True)
    result = []
    for filePath in backup_dir.iterdir():
        if backup_auto_name_match.match(filePath.name):
            result.append(filePath)

    if len(result) < backupCount:
        result = []
    else:
        result.sort()
        result = result[:len(result) - backupCount]

    for filePath in result:
        filePath.unlink()


def restore(archiveName: str, tablenames: list[str] = None):
    try:
        # prepare tablelist
        archive = Archive(backup_dir / archiveName, "r")

        backup_logger.info("Starting restore...")
        backup_logger.info("tables: {}".format(tablenames))

        tablelist = dict()
        for fn in archive.getFileNames():
            tn = convertTablename(fn)
            if tn:
                l = tablelist.setdefault(tn, [])
                l.append(fn)
        for l in tablelist.values():  # sort filenames
            l.sort()
        tl = ujson.dumps(tablelist, ensure_ascii=False, escape_forward_slashes=False, sort_keys=True, indent=4)
        backup_logger.info("Archive '{}' has {}".format(archiveName, tl))

        # check if tablenames valid
        if tablenames is None:
            tablenames = list(tablelist.keys())
        else:
            for tn in tablenames:
                if tn not in tablelist:
                    raise RuntimeError("table '{}' not in backup file".format(tn))

        tablenames = to_topological(tablenames, topological_order)
        if not validate_topological(tablenames, dependencyGraph):
            raise RuntimeError("tablenames does not fulfill dependencies")

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
        if "records" in tablenames or "revisions" in tablenames:
            updateUnfinisheds()
    except RuntimeError as e:
        backup_logger.error(e)
        backup_logger.error("Abort restore")
        raise e
    else:
        backup_logger.info("Restore finished")


def del_backup(archiveName):
    a = backup_dir / archiveName
    if a.is_file():
        a.unlink()
