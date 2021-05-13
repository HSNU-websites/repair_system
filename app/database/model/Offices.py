from .common import db


class Offices(db.Model):
    """
    The table manifests what the office should be responsible for the broken items.
    """

    __tablename__ = "offices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, server_default="0", nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    # item = db.relationship("Items", backref="office")

    def __init__(self, description, sequence=None, **kwargs):
        self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return (
            "Offices(id={id},sequence={sequence},description='{description}')".format(
                **self.__dict__
            )
        )
