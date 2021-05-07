import datetime
import re  # regex
from pathlib import Path

from .model import *
from .Archive import Archive

defaultTables = {Statuses, Items, Buildings,  Users, Records, Revisions}
partition = 1000

backup_dir = Path(__file__).parent/Path("../../Backup")

# mail [].sort(key = lambda s: s[2])
# archiveName -> *.tar.gz / * (a folder)
# filename    -> *.json
# tables      -> [Users]
# tablenames  -> ["users"]

pattern = re.compile(r"^(?P<tableName>[a-z]+)(_\d+-\d+)?.json$")


def convertTablename(filename: str):
    """
    'buildings.json'    -> 'buildings'
    'users_1-1000.json' -> 'users'
    """
    if m := pattern.match(filename):
        return m.group("tableName")


def db_reprTest():
    import flask_sqlalchemy
    import sqlalchemy

    def valid(value):
        return type(value) not in {list, sqlalchemy.orm.state.InstanceState, flask_sqlalchemy.model.DefaultMeta}
    b = True
    for t in defaultTables:
        obj1 = t.query.first()
        obj2 = eval(repr(obj1))
        d1 = {key: value for key, value in obj1.__dict__.items() if valid(value)}
        d2 = {key: value for key, value in obj2.__dict__.items() if valid(value)}
        print(t.__tablename__, d1 == d2)
        b = b and (d1 == d2)
    return b


# def writeArchive(archive: tarfile, filename: str, data: dict) -> None:
#     s = ujson.dumps(data, ensure_ascii=False, escape_forward_slashes=False)
#     encoded = s.encode("utf-8")
#     stream = io.BytesIO(encoded)
#     tarinfo = tarfile.TarInfo(name=filename)
#     tarinfo.size = len(encoded)
#     archive.addfile(tarinfo, stream)


# def readArchive(archive: tarfile.TarFile, filename: str) -> dict:
#     s = archive.extractfile(filename).read().decode("utf-8")
#     return ujson.loads(s)


def getBackups() -> list:
    return list(backup_dir.iterdir())


# def getFileNames(archiveName: str) -> list:
#     with tarfile.open(archiveName, "r:xz") as archive:
#         return archive.getnames()


# def getTableNames(archiveName: str) -> list:
#     l = map(convertTablename, getFileNames(archiveName))
#     return list(set(l))  # unique value


def backup(tables: list[db.Model] = None):  # path not fix
    archiveName = "Backup_{time}.tar.xz".format(
        time=datetime.datetime.now().strftime(timeformat))
    if tables is None:
        tables = defaultTables
    else:
        tables = filter(lambda x: x in defaultTables, tables)

    archive = Archive(backup_dir/archiveName, "w")
    for t in tables:
        max = t.query.order_by(t.id.desc()).first().id
        if max <= partition:
            filename = "{tablename}.json".format(tablename=t.__tablename__)
            final = dict()
            final[t.__tablename__] = [repr(col) for col in t.query.all()]
            archive.write(filename, final)
        else:
            for i in range(1, max+1, partition):
                filename = "{tablename}_{start}-{end}.json".format(
                    tablename=t.__tablename__,
                    start=i, end=i-1+partition)
                final = dict()
                final[t.__tablename__] = [repr(column) for column in t.query.filter(
                    t.id.between(i, i-1+partition)).all()]
                archive.write(filename, final)
    print("Backup finished, file: {}".format(archiveName))

# not finished


# def restore(archiveName: str, tables: list[db.Model] = None):
#     if tables is None:
#         tables = defaultTables
#     tablenames = [t.__tablename__ for t in tables]
#     with tarfile.open(archiveName, "r:xz") as archive:
#         for filename in archive.getnames():
#             if convertTablename(filename) in tablenames:
#                 d = readArchive(archive, filename)
#                 l = list(d.values())[0]
#                 for o in l:
#                     db.session.merge(eval(o))
#     db.session.commit()
