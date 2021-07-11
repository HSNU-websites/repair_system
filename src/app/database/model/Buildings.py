from .common import db


class Buildings(db.Model):
    """
    Buildings.id = 1 will be default building.

    id: PK.
    sequence: The displayed order.
    description: The name of the building.
    """

    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id, description, sequence):
        self.id = id
        self.sequence = sequence
        self.description = description

    def __repr__(self):
        return (
            "Buildings(id={id},sequence={sequence},description='{description}')".format(
                **self.__dict__
            )
        )

    @classmethod
    def new(cls, description, sequence=0):
        return cls(
            id=None,
            description=description[:255],
            sequence=sequence
        )
