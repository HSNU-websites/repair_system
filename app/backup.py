from app.database import *
import datetime
import ujson
import io
import tarfile
import os
import re  # regex

defaultTables = [Statuses, Items, Buildings,  Users, Records, Revisions]
partition = 10

backup_dir = os.path.join("backup")  # need check


# mail [].sort(key = lambda s: s[2])
# archiveName -> *.tar.gz
# fileName    -> *.json
# tables      -> [Users]


def convertTableName(fileName: str):
    """
    'buildings.json'    -> 'buildings'
    'users_1.json' -> 'users'
    """
    if m := convertTableName.pattern.match(fileName):
        return m.group("tableName")


convertTableName.pattern = re.compile(r"^(?P<tableName>[a-z]+)(_\d+)?.json$")


def dbReprTest():
    import sqlalchemy
    import flask_sqlalchemy

    def valid(value):
        return type(value) not in [list, sqlalchemy.orm.state.InstanceState, flask_sqlalchemy.model.DefaultMeta]

    for c in [Statuses, Items, Buildings,  Users, Records, Revisions]:
        obj1 = c.query.first()
        obj2 = eval(repr(obj1))
        d1 = dict()
        d2 = dict()
        for key, value in obj1.__dict__.items():
            if valid(value):
                d1[key] = value
        for key, value in obj2.__dict__.items():
            if valid(value):
                d2[key] = value
        print(c.__tablename__, d1 == d2)


def writeArchive(archive: tarfile, fileName: str, data: dict) -> None:
    s = ujson.dumps(data, ensure_ascii=False)
    encoded = s.encode("utf-8")
    stream = io.BytesIO(encoded)
    tarinfo = tarfile.TarInfo(name=fileName)
    tarinfo.size = len(encoded)
    archive.addfile(tarinfo, stream)


def readArchive(archive: tarfile.TarFile, fileName: str) -> dict:
    s = archive.extractfile(fileName).read().decode("utf-8")
    return ujson.loads(s)


def getBackups() -> list:
    pass


def getFileNames(archiveName: str) -> list:
    with tarfile.open(archiveName, "r:xz") as archive:
        return archive.getnames()


def getTableNames(archiveName: str) -> list:
    l = map(convertTableName, getFileNames(archiveName))
    return list(set(l))  # unique value


def backup(tables: list[db.Model] = None):  # path not fix
    archiveName = "Backup_{time}.tar.xz".format(
        time=datetime.datetime.now().strftime(timeformat))
    if tables is None:
        tables = defaultTables
    else:
        tables = filter(defaultTables.__contains__, tables)
    with tarfile.open(archiveName, "w:xz") as archive:
        for t in tables:
            max = t.query.order_by(t.id.desc()).first().id
            if max <= partition:
                fileName = "{tablename}.json".format(tablename=t.__tablename__)
                final = dict()
                final[t.__tablename__] = [repr(col) for col in t.query.all()]
                writeArchive(archive, fileName, final)
            else:
                for i in range(1, max+1, partition):
                    fileName = "{tablename}_{start}-{end}.json".format(
                        tablename=t.__tablename__,
                        start=i, end=i-1+partition)
                    final = dict()
                    final[t.__tablename__] = [repr(column) for column in t.query.filter(
                        t.id.between(i, i-1+partition)).all()]
                    writeArchive(archive, fileName, final)
    print("Backup finished, file: {}".format(archiveName))


def restore(archiveName: str, tables: list[db.Model] = None):
    if tables is None:
        tables = defaultTables
    tablenames = [t.__tablename__ for t in tables]
    with tarfile.open(archiveName, "r:xz") as archive:
        for fileName in archive.getnames():
            if convertTableName(fileName) in tablenames:
                d = readArchive(archive, fileName)
                l = list(d.values())[0]
                for o in l:
                    db.session.merge(eval(o))
    db.session.commit()
