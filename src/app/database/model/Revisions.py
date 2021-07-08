import datetime
from .common import db, timeformat


class Revisions(db.Model):
    """
    After the admin views the reports, they will make a revision record.
    The table is connected to `Records`, `Users` and `Statuses`.

    id: PK.
    record_id: `id` in `Records` table.
    user_id: `id` in `Users` table.
    status_id: `id` in `Statuses` table.
    insert_time: Revision time. The value will be automatically added.
    description: If the admins fail to find a status for the situation, the field can be used.
    """

    __tablename__ = "revisions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.ForeignKey("records.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    status_id = db.Column(db.ForeignKey("statuses.id"), nullable=False)
    insert_time = db.Column(db.TIMESTAMP, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id, record_id, user_id, status_id, insert_time, description):
        self.id = id
        self.record_id = record_id
        self.user_id = user_id
        self.status_id = status_id
        self.insert_time = datetime.datetime.strptime(insert_time, timeformat)
        self.description = description

    def __repr__(self):
        return (
            "Revisions(id={id},record_id={record_id},user_id={user_id},status_id={status_id},insert_time='{mytime}',description='{description}')"
            .format(mytime=self.insert_time.strftime(timeformat), **self.__dict__)
        )

    @classmethod
    def new(cls, record_id, user_id, status_id, description, insert_time=None):
        if insert_time is None:
            insert_time = datetime.datetime.now().strftime(timeformat)

        return cls(
            id=None,
            record_id=record_id,
            user_id=user_id,
            status_id=status_id,
            insert_time=insert_time,
            description=description[:255]
        )
