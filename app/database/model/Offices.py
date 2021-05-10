from .common import db


class Offices(db.Model):
    """
    The table manifests what the office should be responsible for the broken items.
    """

    __tablename__ = "offices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    item = db.relationship("Items", backref="office")

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Offices.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
            # flush
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Items(id={id},sequence={sequence},description='{description}')".format(
            **self.__dict__
        )
