from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
db = SQLAlchemy()
timeformat = "%Y-%m-%dT%H-%M-%S"

passwd_context = CryptContext(  # First scheme will be default
    schemes=["pbkdf2_sha256", "sha512_crypt"],
    deprecated="auto"
)
