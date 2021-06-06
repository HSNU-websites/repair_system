from os import getenv, urandom


class Config:
    SECRET_KEY = urandom(16)
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "HSNU"
    # APScheduler
    SCHEDULER_API_ENABLED = True
    # Cache
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 0  # Never timeout
    CACHE_THRESHOLD = 5000


class Development(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    DEBUG = True
    ENV = "development"


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    TESTING = True
    DEBUG = True
    ENV = "testing"
    RECAPTCHA_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False


class Production(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}".format(
        DB_USER=getenv("DB_USER"),
        DB_PASSWORD=getenv("DB_PASSWORD"),
        DB_HOST=getenv("DB_HOST"),
        DB_DATABASE=getenv("DB_DATABASE"),
    )
    ENV = "production"


config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}
