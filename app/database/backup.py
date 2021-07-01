import datetime
import logging
import re  # regex
from pathlib import Path

import ujson
from app.myhandler import MyTimedRotatingFileHandler

from .Archive import Archive
from .common import cache
from .db_helper import updateUnfinisheds
from .model import *

defaultTables = idTables
partition = 10000

backup_dir = Path("backup").resolve()  # absolute path to backup directory

# mail [].sort(key = lambda s: s[2])
# archiveName -> *.tar.gz / * (a folder)
# filename    -> *.json
# tables      -> [Users]
# tablenames  -> ["users"]

backup_log_handler = MyTimedRotatingFileHandler(
    "log/backup.log",
    "log/backup_%Y-%m-%d.log",
    when="MIDNIGHT",
    backupCount=14,
    encoding="UTF-8",
    delay=False,
    utc=False,
)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
backup_log_handler.setFormatter(format)
backup_log_handler.setLevel(logging.INFO)
#  backup_log_handler handles log if log.level > INFO

backup_logger = logging.getLogger('backup')
backup_logger.addHandler(backup_log_handler)
backup_logger.setLevel(logging.INFO)
# backup_logger pass log to handlers if log.level > INFO

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

    backup_logger.info("Starting backup...")
    backup_logger.info("tables: {}".format(tablenames))

    if tablenames is None:
        tablenames = topological_order
        backup_logger.info("use default tables: {}".format(tablenames))
    else:
        for tn in tablenames:
            if tn not in idTables:
                err = "table '{}' not available".format(tn)
                backup_logger.error(err)
                raise RuntimeError(err)
        tablenames = to_topological(tablenames, topological_order)
        if not validate_topological(tablenames, dependencyGraph):
            err = "tablenames does not fulfill dependencies"
            backup_logger.error(err)
            raise RuntimeError(err)

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
    backup_logger.info("Backup finished, file: {}".format(archiveName))


def restore(archiveName: str, tablenames: list[str] = None):
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
                err = "table '{}' not in backup file".format(tn)
                backup_logger.error(err)
                raise RuntimeError(err)

    tablenames = to_topological(tablenames, topological_order)
    if not validate_topological(tablenames, dependencyGraph):
        err = "tablenames does not fulfill dependencies"
        backup_logger.error(err)
        raise RuntimeError(err)

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

    backup_logger.info("Restore finished")


def del_backup(archiveName):
    a = backup_dir / archiveName
    if a.is_file():
        a.unlink()
