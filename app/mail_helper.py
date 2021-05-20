from datetime import datetime, timedelta, date
from flask_mail import Message
from flask import current_app
from .database import db
from .database.db_helper import get_admin_emails
from .database.model import Users, Buildings, Items, Records, Unfinisheds, Offices
from . import mail


def send_report_mail(user_id, building_id, location, item_id, description):
    subject = "報修成功通知"
    user = db.session.query(
        Users.username, Users.name).filter_by(id=user_id).first()
    building = db.session.query(
        Buildings.description).filter_by(id=building_id).first()
    item = db.session.query(
        Items.office_id, Items.description).filter_by(id=item_id).first()
    office = db.session.query(
        Offices.description).filter_by(id=item.office_id).first()
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
        office=office.description,
        description=description,
    )
    if user.email:
        # For admins
        recipients = [user.email]
    else:
        # For normal students
        recipients = [user.username + "@gs.hs.ntnu.edu.tw"]

    # do not send email in development
    if current_app.config["ENV"] != "production":
        print("not sending mail since ENV={ENV}\n"
              "subject: {subject}\n"
              "recipients: {recipients}\n"
              "content: \n{content}"
              .format(ENV=current_app.config["ENV"], subject=subject, recipients=recipients, content=content)
              )
        return

    msg = Message(subject, recipients=recipients)
    msg.html = content
    mail.send(msg)


def send_daily_mail():
    # prepare data
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = (today - timedelta(days=1))
    seven_days = (today - timedelta(days=7))

    # todo ordered by offices.sequence
    result = [(row.id, row.description, [[], [], []])
              for row in db.session.query(Offices.id, Offices.description)
              .all()]

    # query object
    unfin_query = db.session.query(Unfinisheds.record_id)
    for id, _, value in result:
        item_query = db.session.query(Items.id).filter(Items.office_id == id)
        records = (
            Records.query.filter(Records.id.in_(unfin_query))
                   .filter(Records.item_id.in_(item_query))
                   .order_by(Records.time.desc())
                   .all()
        )
        for row in records:
            if row.time > today:
                pass  # today
            elif row.time > yesterday:
                value[0].append(row)  # yesterday
            elif row.time > seven_days:
                value[1].append(row)  # 2-7 days
            else:
                value[2].append(row)  # 7 days and before
    # print(result)

    # send mail
    subject = "%s 報修列表" % datetime.now().strftime("%Y/%m/%d")
    record = ""
    for id, description, value in result:
        record += "<div><b>%s</b></div>" % description
        record += "<div>昨日新增: </div>"
        for row in value[0]:
            record += "<div>%s %s</div>" % (
                row.time.strftime("%Y-%m-%dT%H-%M-%S"), row.description
            )

        record += "<div>七天內未完成: </div>"
        for row in value[1]:
            record += "<div>%s %s</div>" % (
                row.time.strftime("%Y-%m-%dT%H-%M-%S"), row.description
            )

        record += "<div>七天以上未完成: </div>"
        for row in value[2]:
            record += "<div style='color: red'>%s %s</div>" % (
                row.time.strftime("%Y-%m-%dT%H-%M-%S"), row.description
            )
    content = """
    <h3>每日報修:</h3>
    <div>未完成以紅色表示</div>
        {record}

    <footer>此為系統自動寄送郵件，不須回覆</footer>
    """.format(
        record=record
    )
    recipients = get_admin_emails()
    msg = Message(subject, recipients=recipients)
    msg.html = content
    mail.send(msg)
    current_app.logger.info("Send daily report mail.")
