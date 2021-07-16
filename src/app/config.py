from os import getenv, urandom


class Config:
    # Flask-Caching
    CACHE_DEFAULT_TIMEOUT = 0  # Never timeout
    CACHE_THRESHOLD = 5000
    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "HSNU"
    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-WTF reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = getenv("RECAPTCHA_PRIVATE_KEY")


class Development(Config):
    # Flask
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "dhfkjgruytv4yntcm94[g"
    # Flask-APScheduler
    SCHEDULER_API_ENABLED = True
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    CACHE_TYPE = "SimpleCache"


class Testing(Config):
    # Flask
    ENV = "testing"
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = "dhfkjgruytv4yntcm94[g"
    TESTING = True
    # Flask-Caching
    CACHE_TYPE = "SimpleCache"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Flask-WTF
    WTF_CSRF_ENABLED = False


class Production(Config):
    # Flask
    ENV = "production"
    PREFERRED_URL_SCHEME = "https"
    SECRET_KEY = urandom(32)
    # Flask-Caching
    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "/dev/shm/repair_system/"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}?charset=utf8mb4".format(
        DB_USER=getenv("DB_USER"),
        DB_PASSWORD=getenv("DB_PASSWORD"),
        DB_HOST=getenv("DB_HOST"),
        DB_DATABASE=getenv("DB_DATABASE"),
    )


config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}
