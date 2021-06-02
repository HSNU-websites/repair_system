import logging

from app.myhandler import MyTimedRotatingFileHandler
from . import backup, db_helper
from .model import db, timeformat, filetimeformat
from .common import cache

__all__ = [db, backup, db_helper, cache]

sql_log_handler = MyTimedRotatingFileHandler(
    "log/SQL.log",
    "log/SQL_%Y-%m-%d.log",
    when="MIDNIGHT",
    backupCount=14,
    encoding="UTF-8",
    delay=False,
    utc=False,
)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
sql_log_handler.setFormatter(format)
sql_log_handler.setLevel(logging.INFO)
# sql_log_handler handles log if log.level > INFO

sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.addHandler(sql_log_handler)
sql_logger.setLevel(logging.DEBUG)
# sql_logger pass log to handlers if log.level > DEBUG
