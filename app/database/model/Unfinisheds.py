from .common import db


class Unfinisheds(db.Model):
    """
    This TABLE is used to optimize query.
    Do not need to backup.
    """

    __tablename__ = "unfinisheds"
    record_id = db.Column(db.ForeignKey("records.id"), primary_key=True)
    # record = db.relationship("Records")

    def __init__(self, record_id):
        self.record_id = record_id

    def __repr__(self):
        return "Unfinisheds(record_id={record_id})".format(**self.__dict__)
