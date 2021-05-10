import logging
import re  # regex
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from . import backup, db_helper
from .model import db, timeformat

__all__ = [db, backup, db_helper]


# def my_namer(default_name):
#     # This will be called when doing the log rotation
#     # default_name is the default filename that would be assigned, e.g. Rotate_Test.txt.YYYY-MM-DD
#     # Do any manipulations to that name here, for example this changes the name to Rotate_Test.YYYY-MM-DD.txt
#     base_filename, ext, date = default_name.split(".")
#     return f"{base_filename}_{date}.{ext}"

# todo rewrite log handler
Path("log").mkdir(parents=True, exist_ok=True)
sql_log_handler = TimedRotatingFileHandler(
    r"log/SQL.log",
    when="D",
    interval=1,
    backupCount=2,
    encoding="UTF-8",
    delay=False,
    utc=False,
)

# sql_log_handler.suffix = timeformat
# sql_log_handler.extMatch = re.compile(timeformat_re_str+".log")
# sql_log_handler.namer = my_namer

format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
sql_log_handler.setFormatter(format)
sql_log_handler.setLevel(logging.INFO)

sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.addHandler(sql_log_handler)
sql_logger.setLevel(logging.DEBUG)
