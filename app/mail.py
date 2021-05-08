from flask_mail import Message
from .database.model import Users, Buildings, Items
from . import mail


def send_report_mail(user_id, building_id, location, item_id, description):
    subject = "報修成功通知"
    user = Users.query.filter_by(id=user_id).first()
    building = Buildings.query.filter_by(id=building_id).first()
    item = Items.query.filter_by(id=item_id).first()
    content = """
    報修:
        報修人: {user}
        大樓: {building}
        地點: {location}
        損壞物件: {item} ({office})
        敘述: {description}

    此為系統自動寄送郵件，不須回覆
    """.format(
        user=" ".join([user.username, user.name]),
        building=building.description,
        location=location,
        item=item.description,
        office=item.office.description,
        description=description,
    )
    if user.email:
        recipients = [user.email]
    else:
        recipients = [user.username + "@gs.hs.ntnu.edu.tw"]

    msg = Message(subject, sender="HSNU", recipients=recipients)
    msg.body = content
    mail.send(msg)