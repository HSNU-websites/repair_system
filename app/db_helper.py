from .database import db, Statuses, Items, Buildings, Admins, Users, Records, Revisions


def render_statuses():
    statuses = Statuses.query.all()
    return [status.description for status in statuses]


def render_items():
    items = Items.query.all()
    return [item.description for item in items]


def render_buildings():
    buildings = Buildings.query.all()
    return [building.description for building in buildings]
