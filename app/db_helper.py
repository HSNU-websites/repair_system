from .database import Admins
from .database import Buildings
from .database import db
from .database import Items
from .database import Records
from .database import Revisions
from .database import Statuses
from .database import Users


def render_statuses():
    statuses = Statuses.query.all()
    return [status.description for status in statuses]


def render_items():
    items = Items.query.all()
    return [item.description for item in items]


def render_buildings():
    buildings = Buildings.query.all()
    return [building.description for building in buildings]
