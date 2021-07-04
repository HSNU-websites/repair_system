from .common import db


class Offices(db.Model):
    """
    The table manifests what the office should be responsible for the broken items.
    """

    __tablename__ = "offices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id, description, sequence):
        self.id = id
        self.sequence = sequence
        self.description = description

    def __repr__(self):
        return (
            "Offices(id={id},sequence={sequence},description='{description}')".format(
                **self.__dict__
            )
        )

    @classmethod
    def new(cls, description, sequence=0):
        return Offices(
            id=None,
            description=description[:255],
            sequence=sequence
        )
