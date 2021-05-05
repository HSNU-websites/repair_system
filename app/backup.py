from app.database import *
import datetime
import ujson
import io
import tarfile
import os
import lzma
import re  # regex


tables = [Statuses, Items, Buildings,  Users, Records, Revisions]
backup_dir = os.path.join("backup")  # need check
partition = 10

# mail [].sort(key = lambda s: s[2])


def tableName(filename: str):
    """
    'buildings.json'    -> 'buildings'
    'users_1-1000.json' -> 'users'
    """
    if m := tableName.pattern.match(filename):
        return m.group("name")


tableName.pattern = re.compile(r"^(?P<name>[a-z]+)(_\d+-\d+)?.json$")


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


def write(archive: tarfile, name: str, data: str) -> None:
    encoded = data.encode("utf-8")
    stream = io.BytesIO(encoded)
    tarinfo = tarfile.TarInfo(name=name)
    archive.addfile(tarinfo, stream)


def read(archive: tarfile, name: str) -> str:
    return archive.extractfile(name).read().decode("utf-8")


def getBackups() -> list:
    pass


def getTables(name: str) -> list:
    with tarfile.open(name, "r:xz") as archive:
        return archive.getnames()

def backup():
    final = dict()
    name = "Backup_{time}.tar.xz".format(
        time=datetime.datetime.now().strftime(timeformat))

    for t in tables:
        final[t.__tablename__] = [repr(col) for col in t.query.all()]

    s = ujson.dumps(final, ensure_ascii=False)
    with lzma.LZMAFile(name, "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, preset=7) as file:
        file.write(s.encode("utf-8"))
    print("Backup finished, file: {}".format(name))

    # os.
# pagination


def restore(name):
    with lzma.LZMAFile(name, "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, preset=7) as file:
        file.write(s.encode("utf-8"))
    pass
