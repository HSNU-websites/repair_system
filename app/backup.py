from app.database import *
import json
import lzma

tables = [Statuses, Items, Buildings,  Users, Records, Revisions]


def backup():
    final = dict()
    for table in tables:
        final[table.__tablename__] = [
            repr(column) for column in table.query.all()]

    s = json.dumps(final, separators=(',', ':'))
    com = lzma.compress(s.encode('utf-8'))
    with lzma.LZMAFile("backup.json.xz", "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, preset=8):
        pass
    print(s, len(s), len(com))
    return s


def restore():
    pass
