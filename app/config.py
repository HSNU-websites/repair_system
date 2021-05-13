from os import getenv


class Config:
    SECRET_KEY = getenv("SECRET_KEY")
    # RECAPTCHA
    RECAPTCHA_ENABLED = True
    RECAPTCHA_PUBLIC_KEY = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = getenv("RECAPTCHA_PRIVATE_KEY")
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    # Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "HSNU"
    # APScheduler
    SCHEDULER_API_ENABLED = True


class Development(Config):
    DEBUG = True
    ENV = "development"


class Testing(Config):
    TESTING = True
    DEBUG = True
    ENV = "testing"
    RECAPTCHA_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False


class Production(Config):
    ENV = "development"


config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}
