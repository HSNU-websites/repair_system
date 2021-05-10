from .common import db


class Statuses(db.Model):
    """
    Statuses.id = 1 will be default item.

    id: PK.
    sequence: The displayed order.
    description: The name of the building.
    """

    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, server_default="0",
                         nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return (
            "Statuses(id={id},sequence={sequence},description='{description}')"
            .format(**self.__dict__)
        )
