from flask import Blueprint, Flask
from flask_login import LoginManager
from config import config

login_manager = LoginManager()

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])
    
    login_manager.init_app(app)
    
    return app