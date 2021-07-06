import datetime
import logging
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from .database import db
from .database.db_helper import get_admin_emails
from .database.model import (
    Buildings,
    Items,
    Offices,
    Records,
    Unfinisheds,
    Users,
    timeformat,
)

mail_logger = logging.getLogger("mail")


def send_mail(subject, recipients, html):
    """
    Send mail and log to mail_logger.
    """
    mail_logger.info(
        "Sending mail...\n"
        "Subject: {subject}\n"
        "Bcc: {recipients}\n"
        "Html: {html}".format(subject=subject, recipients=recipients, html=html)
    )

    # do not send email in development
    if current_app.config["ENV"] != "production":
        mail_logger.info(
            "Not send mail since ENV={ENV}".format(ENV=current_app.config["ENV"])
        )
    else:
        sender = (
            current_app.config["MAIL_DEFAULT_SENDER"],
            current_app.config["MAIL_USERNAME"],
        )
        msg = Message(subject=subject, bcc=recipients, html=html, sender=sender)
        try:
            mail.send(msg)
        except Exception as e:
            mail_logger.exception(e)
        else:
            mail_logger.info("Mail sent successfully")


def send_report_mail(user_id, building_id, location, item_id, description):
    user = (
        db.session.query(Users.username, Users.name, Users.email)
        .filter_by(id=user_id)
        .first()
    )
    building = db.session.query(Buildings.description).filter_by(id=building_id).first()
    item = (
        db.session.query(Items.office_id, Items.description)
        .filter_by(id=item_id)
        .first()
    )
    office = db.session.query(Offices.description).filter_by(id=item.office_id).first()

    subject = "報修成功通知"
    content = render_template(
        "report_mail.html",
        user=" ".join([user.username, user.name]),
        building=building.description,
        location=location,
        item=item.description,
        office=office.description,
        description=description,
    )
    if user.email:
        # For admins
        recipients = [user.email]
    else:
        # For normal students
        recipients = [user.username + "@gs.hs.ntnu.edu.tw"]

    send_mail(subject=subject, recipients=recipients, html=content)


def send_daily_mail():
    # prepare data
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - datetime.timedelta(days=1)
    seven_days = today - datetime.timedelta(days=7)

    # get offices
    # (office.id, office.description, [ [yesterday], [2-7 days], [7 days and before] ] )
    result = [
        (row.id, row.description, [[], [], []])
        for row in db.session.query(Offices.id, Offices.description)
        .order_by(Offices.sequence)
        .all()
    ]

    # query object
    unfin_query = db.session.query(Unfinisheds.record_id)
    for id, _, value in result:
        item_query = db.session.query(Items.id).filter(Items.office_id == id)
        records = (
            Records.query.filter(Records.id.in_(unfin_query))
            .filter(Records.item_id.in_(item_query))
            .order_by(Records.id.desc())
            .all()
        )
        for row in records:
            if row.insert_time >= today:
                pass  # today
            elif row.insert_time >= yesterday:
                value[0].append(row)  # yesterday
            elif row.insert_time >= seven_days:
                value[1].append(row)  # 2-7 days
            else:
                value[2].append(row)  # 7 days and before

    # send mail
    today = today.strftime("%Y/%m/%d")
    subject = f"{today} 報修列表"
    content = render_template("daily_mail.html", records=result, timeformat=timeformat)
    send_mail(subject=subject, recipients=get_admin_emails(), html=content)
