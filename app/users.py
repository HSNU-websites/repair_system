from flask_login import UserMixin
from . import login_manager


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user
