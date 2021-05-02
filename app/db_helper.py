from .database import (Admins, Buildings, Items, Records, Revisions, Statuses,
                       Users, db)


def render_statuses():
    statuses = Statuses.query.all()
    return [status.description for status in statuses]


def render_items():
    items = Items.query.all()
    return [item.description for item in items]


def render_buildings():
    buildings = Buildings.query.all()
    return [building.description for building in buildings]
