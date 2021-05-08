import datetime
from .common import db, timeformat


class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.ForeignKey("items.id"), nullable=False)
    building_id = db.Column(db.ForeignKey("buildings.id"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False, index=True
    )
    description = db.Column(db.String(255), nullable=False)
    revisions = db.relationship("Revisions")

    def __init__(self, user_id, item_id, building_id, location, description, **kwargs):
        self.user_id = user_id
        self.item_id = item_id
        self.building_id = building_id
        self.location = location
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "time" in kwargs:
            self.time = datetime.datetime.strptime(kwargs["time"], timeformat)

    def __repr__(self):
        return "Records(id={id},user_id={user_id},item_id={item_id},building_id={building_id},location='{location}',time='{mytime}',description='{description}')".format(mytime=self.time.strftime(timeformat), **self.__dict__)
