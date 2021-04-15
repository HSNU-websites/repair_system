from os import getenv

class Config:
    SECRET_KEY = getenv("SECRET_KEY")
    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = getenv("RECAPTCHA_SITE_KEY")
    RECAPTCHA_SECRET_KEY = getenv("RECAPTCHA_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    # MAIL
    
class Development(Config):
    DEBUG = True
    ENV = "development"
    
class Testing(Config):
    TESTING = True
    ENV = "testing"
    
class Production(Config):
    ENV = "development"
    
config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}