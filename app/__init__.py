from flask import Blueprint, Flask
from flask_login import LoginManager
from .config import config

login_manager = LoginManager()


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[env])

    login_manager.init_app(app)
    
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    from .user import user_bp
    app.register_blueprint(user_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    return app