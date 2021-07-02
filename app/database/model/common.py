from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

db = SQLAlchemy()
timeformat = r"%Y-%m-%dT%H:%M:%S"
dateformat = r"%Y-%m-%d"
filetimeformat = r"%Y-%m-%dT%H-%M-%S"
timeformat_re_str = r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}"
finishedStatus_id = 2

passwd_context = CryptContext(  # First scheme will be default
    schemes=["pbkdf2_sha256", "sha512_crypt"], deprecated="auto"
)


def get_dict(row):
    """
    Get pure dict from table without relationship.
    datetime.datetime will be converted to str
    """
    import datetime

    def process_value(value):
        if isinstance(value, datetime.datetime):
            return value.strftime(timeformat)
        else:
            return value

    if isinstance(row, db.Model):
        return {
            key: process_value(row.__dict__[key])
            for key in row.__mapper__.columns.keys()
        }
    else:
        return {}


def get_foreign_key_dependencies(table) -> list:
    dependencies = []
    for fk in table.__table__.foreign_keys:
        tablename, colname = fk.target_fullname.split(".")
        dependencies.append(tablename)
    return dependencies


def topological_sort(graph) -> list:
    """
    return tablenames in topological order (build)
    """

    def dfs(graph: dict, node, walking: set, order: list, visited: set):
        if node in walking:  # circular dependency
            return False
        if node in visited:
            return True
        walking.add(node)
        for child in graph[node]:
            if not dfs(graph, child, walking, order, visited):
                return False
        walking.remove(node)
        visited.add(node)
        order.append(node)
        return True

    walking = set()
    order = []
    visited = set()

    for node in graph.keys():
        if not dfs(graph, node, walking, order, visited):
            return None

    return order


def to_topological(target, sample):
    s = set(target)
    result = []
    for node in sample:
        if node in s:
            result.append(node)
            s.remove(node)
    for node in s:  # if node is not in sample, assume it does not depand on anyone.
        result.append(node)
    return result


def validate_topological(target, graph):
    s = set()
    for node in target:
        for child in graph[node]:
            if child not in s:
                return False
        s.add(node)
    return True
