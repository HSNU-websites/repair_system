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
    insert_time: Revision time. The value will be automatically added.
    update_time: Should be updated when new revision is added.
    description: The detailed description about the broken items and is written by the reporter.
    """

    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    item_id = db.Column(db.ForeignKey("items.id"), nullable=False)
    building_id = db.Column(db.ForeignKey("buildings.id"), nullable=False)
    insert_time = db.Column(db.TIMESTAMP, nullable=False)
    update_time = db.Column(db.TIMESTAMP, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id, user_id, item_id, building_id, insert_time, update_time, location, description):
        self.id = id
        self.user_id = user_id
        self.item_id = item_id
        self.building_id = building_id
        self.insert_time = insert_time
        self.update_time = update_time
        self.location = location
        self.description = description

    def __repr__(self):
        return (
            "Records(id={id},user_id={user_id},item_id={item_id},building_id={building_id},location='{location}',insert_time='{myinserttime}',update_time='{myupdatetime}',description='{description}')"
            .format(myinserttime=self.insert_time.strftime(timeformat), myupdatetime=self.update_time.strftime(timeformat), **self.__dict__)
        )

    @classmethod
    def new(cls, user_id, item_id, building_id, location="", description="", insert_time=None, update_time=None):
        if insert_time is not None:
            it = datetime.datetime.strptime(insert_time, timeformat)
        else:
            it = datetime.datetime.now().replace(microsecond=0)

        if update_time is not None:
            ut = datetime.datetime.strptime(update_time, timeformat)
        else:
            ut = it

        return cls(
            id=None,
            user_id=user_id,
            item_id=item_id,
            building_id=building_id,
            insert_time=it,
            update_time=ut,
            location=location,
            description=description
        )
