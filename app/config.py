from os import getenv


class Config:
    SECRET_KEY = getenv("SECRET_KEY")
    # RECAPTCHA
    RECAPTCHA_ENABLED = True
    RECAPTCHA_PUBLIC_KEY = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_SECRET_KEY = getenv("RECAPTCHA_SECRET_KEY")
    RECAPTCHA_OPTIONS = {"theme": "black"}
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    # Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")


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
