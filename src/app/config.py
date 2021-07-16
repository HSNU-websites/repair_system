from os import getenv, urandom


class Config:
    SECRET_KEY = urandom(32)
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}?charset=utf8mb4".format(
        DB_USER=getenv("DB_USER"),
        DB_PASSWORD=getenv("DB_PASSWORD"),
        DB_HOST=getenv("DB_HOST"),
        DB_DATABASE=getenv("DB_DATABASE"),
    )
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
    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "/dev/shm/repair_system/"
    CACHE_DEFAULT_TIMEOUT = 0  # Never timeout
    CACHE_THRESHOLD = 5000
    # reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = getenv("RECAPTCHA_PRIVATE_KEY")


class Development(Config):
    ENV = "development"
    SECRET_KEY = "dhfkjgruytv4yntcm94[g"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    CACHE_TYPE = "SimpleCache"
    DEBUG = True


class Testing(Config):
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CACHE_TYPE = "SimpleCache"
    TESTING = True
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False


class Production(Config):
    ENV = "production"
    PREFERRED_URL_SCHEME = "https"


config = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}
