from . import login_manager
from .db_helper import load_user


@login_manager.user_loader
def load(user_id):
    return load_user(user_id)
