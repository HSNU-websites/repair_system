import datetime
from .common import db, timeformat


class Records(db.Model):
    """
    The table stores all report records.
    The table is connected to `Users`, `Items` and `Buildings`.

    id: PK.
    user_id: `id` in `Users` table.
    item_id: `id` in `Items` table.
    building_id: `id` in `Buildings` table.
    location: The detailed place which is written by the reporter.
    time: Revision time. The value will be automatically added.
    description: The detailed description about the broken items and is written by the reporter.
    """

    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    item_id = db.Column(db.ForeignKey("items.id"), nullable=False)
    building_id = db.Column(db.ForeignKey("buildings.id"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    insert_time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False
    )
    update_time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False, index=True
    )
    description = db.Column(db.String(255), nullable=False)
    # revisions = db.relationship("Revisions")

    def __init__(self, user_id, item_id, building_id, location, description, **kwargs):
        self.user_id = user_id
        self.item_id = item_id
        self.building_id = building_id
        self.location = location
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "insert_time" in kwargs:
            self.insert_time = datetime.datetime.strptime(
                kwargs["insert_time"], timeformat)
        if "update_time" in kwargs:
            self.update_time = datetime.datetime.strptime(
                kwargs["update_time"], timeformat)

    def __repr__(self):
        return (
            "Records(id={id},user_id={user_id},item_id={item_id},building_id={building_id},location='{location}',insert_time='{myinserttime}',update_time='{myupdatetime}',description='{description}')"
            .format(myinserttime=self.insert_time.strftime(timeformat), myupdatetime=self.update_time.strftime(timeformat), **self.__dict__)
        )

    @staticmethod
    def update(id):
        Records.query.filter_by(id=id).update(
            {"update_time": db.text("CURRENT_TIMESTAMP")})
