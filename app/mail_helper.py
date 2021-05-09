from datetime import datetime, timedelta
from flask_mail import Message
from flask import current_app
from .database import db
from .database.db_helper import get_admin_emails
from .database.model import Users, Buildings, Items, Records, Unfinisheds, Offices
from . import mail


def send_report_mail(user_id, building_id, location, item_id, description):
    subject = "報修成功通知"
    user = Users.query.filter_by(id=user_id).first()
    building = Buildings.query.filter_by(id=building_id).first()
    item = Items.query.filter_by(id=item_id).first()
    content = """
    <h3>報修:</h3>
    <main>
        <div><b>報修人:</b> {user}</div>
        <div><b>大樓:</b> {building}</div>
        <div><b>地點:</b> {location}</div>
        <div><b>損壞物件:</b> {item} ({office})</div>
        <div><b>敘述:</b> {description}</div>
    </main>
    <footer>此為系統自動寄送郵件，請勿回覆</footer>
    """.format(
        user=" ".join([user.username, user.name]),
        building=building.description,
        location=location,
        item=item.description,
        office=item.office.description,
        description=description,
    )
    if user.email:
        # For admins
        recipients = [user.email]
    else:
        # For normal students
        recipients = [user.username + "@gs.hs.ntnu.edu.tw"]

    msg = Message(subject, recipients=recipients)
    msg.html = content
    mail.send(msg)


def dm():
    items = {row.id: row.office_id
             for row in db.session.query(Items.id, Items.office_id).all()
             }
    unfinished_records = [r for r in Records.query.filter(Records.id.in_(Unfinisheds))]
    result = {row.id: [[], [], []]
              for row in db.session.query(Offices.id).all()}
    pass


def send_daily_mail():
    subject = "%s 報修列表" % datetime.now().strftime("%Y/%m/%d")
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    seven_days = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    offices = [(office.id, office.description)
               for office in Offices.query.all()]
    unfinisheds = [unfinished for unfinished in Unfinisheds.query.all()]
    records = []
    for office_id, office_description in offices:
        record = "<div><b>%s</b></div>" % office_description

        record += "<div>昨日新增: </div>"
        record_yesterday = set(
            db.session.query(Records)
            .filter(Records.time.between(yesterday, yesterday))
            .order_by("time")
            .all()
        )
        # Temporarily storing the records that have been written in the email.
        finished = []
        for r in record_yesterday:
            if r.id in [unfinished.record_id for unfinished in unfinisheds]:
                record += "<div style='color: red'>%s %s</div>" % (
                    r.time,
                    r.description,
                )
                finished.append(r.id)
            else:
                record += "<div>%s %s</div>" % (r.time, r.description)
        unfinisheds = filter(
            lambda unfinished: unfinished.record_id not in finished, unfinisheds)

        record += "<div>七天內未完成: </div>"
        finished = []
        for unfinished in unfinisheds:
            if unfinished.record.item.office.id == office_id and unfinished.record.time > datetime.now() - timedelta(days=7):
                record += "<div style='color: red'>%s %s</div>" % (
                    unfinished.record.time,
                    unfinished.record.description,
                )
                finished.append(unfinished.record_id)
        unfinisheds = filter(
            lambda unfinished: unfinished.record_id not in finished, unfinisheds)

        record += "<div>七天以上未完成: </div>"
        for unfinished in unfinisheds:
            if unfinished.record.item.office.id == office_id:
                record += "<div style='color: red'>%s %s</div>" % (
                    unfinished.record.time, unfinished.record.description)

        records.append(record)
    content = """
    <h3>每日報修:</h3>
    <div>未完成以紅色表示</div>
        {records}

    <footer>此為系統自動寄送郵件，不須回覆</footer>
    """.format(
        records
    )
    print(content)
    return
    recipients = get_admin_emails()
    msg = Message(subject, recipients=recipients)
    msg.html = content
    mail.send(msg)
    current_app.logger.info("Send daily report mail.")
