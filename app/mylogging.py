import logging

from flask import has_request_context, request

from .myhandler import MyTimedRotatingFileHandler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

# handler.setLevel(logging.INFO): handles log if log.level > INFO
#  logger.setLevel(logging.INFO): pass log to handlers if log.level > INFO


def init_logging(app):
    # app log
    access_log_handler = MyTimedRotatingFileHandler(
        "log/access.log",
        "log/access_%Y-%m-%d.log",
        when="MIDNIGHT",
        backupCount=14,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    access_log_formatter = RequestFormatter(
        "[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s: %(message)s"
    )
    access_log_handler.setFormatter(access_log_formatter)
    access_log_handler.setLevel(logging.INFO)

    app.logger.handlers = []  # remove stream handler
    app.logger.addHandler(access_log_handler)
    app.logger.setLevel(logging.INFO)

    # sqlalchemy log
    sql_log_handler = MyTimedRotatingFileHandler(
        "log/SQL.log",
        "log/SQL_%Y-%m-%d.log",
        when="MIDNIGHT",
        backupCount=14,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    sql_log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    sql_log_handler.setFormatter(sql_log_formatter)
    sql_log_handler.setLevel(logging.INFO)

    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.addHandler(sql_log_handler)
    sql_logger.setLevel(logging.INFO)

    # backup log
    backup_log_handler = MyTimedRotatingFileHandler(
        "log/backup.log",
        "log/backup_%Y-%m-%d.log",
        when="MIDNIGHT",
        backupCount=14,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    backup_log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    backup_log_handler.setFormatter(backup_log_formatter)
    backup_log_handler.setLevel(logging.INFO)

    backup_logger = logging.getLogger("backup")
    backup_logger.addHandler(backup_log_handler)
    backup_logger.setLevel(logging.INFO)

    # mail log
    mail_log_handler = MyTimedRotatingFileHandler(
        "log/mail.log",
        "log/mail_%Y-%m-%d.log",
        when="MIDNIGHT",
        backupCount=14,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    mail_log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    mail_log_handler.setFormatter(mail_log_formatter)
    mail_log_handler.setLevel(logging.INFO)

    mail_logger = logging.getLogger("mail")
    mail_logger.addHandler(mail_log_handler)
    mail_logger.setLevel(logging.INFO)
