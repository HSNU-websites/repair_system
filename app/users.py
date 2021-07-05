from functools import wraps
from flask_login import current_user
from . import login_manager
from .database.db_helper import load_user


@login_manager.user_loader
def load(user_id):
    return load_user(int(user_id))


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_active:
            if current_user.is_admin:
                return func(*args, **kwargs)
            else:
                return login_manager.forbidden()
        else:
            return login_manager.unauthorized()            

    return decorated_view
