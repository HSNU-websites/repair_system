from flask_login import UserMixin
from . import login_manager


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(username):
    user = User()
    user.id = username
    return user
