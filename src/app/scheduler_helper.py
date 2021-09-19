from functools import wraps

from flask_apscheduler import APScheduler as _BaseAPScheduler

from . import mail_helper
from .database import backup_helper


class APScheduler(_BaseAPScheduler):
    def with_app_context(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.app.app_context():
                return func(*args, **kwargs)
        return wrapper


scheduler = APScheduler()


@scheduler.task("cron", day="*", hour="7")
@scheduler.with_app_context
def send_daily_mail():
    return mail_helper.send_daily_mail()

@scheduler.task("cron", day="*", hour="3")
@scheduler.with_app_context
def daily_backup():
    return backup_helper.scheduled_backup()
