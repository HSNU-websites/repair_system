from functools import wraps
from flask_login import current_user
from . import login_manager
from .database.db_helper import load_user


@login_manager.user_loader
def load(user_id):
    return load_user(user_id)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            if current_user.isAdmin:
                return func(*args, **kwargs)
            else:
                return login_manager.unauthorized()
        except:
            return login_manager.unauthorized()

    return decorated_view
