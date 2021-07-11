from .common import db


class Items(db.Model):
    """
    Items.id = 1 will be default item.

    id: PK.
    sequence: The displayed order.
    office_id: The office it belongs to.
    description: The name of the item.
    """

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=False, index=True)
    office_id = db.Column(db.ForeignKey("offices.id"), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id, sequence, office_id, description):
        self.id = id
        self.sequence = sequence
        self.office_id = office_id
        self.description = description

    def __repr__(self):
        return (
            "Items(id={id},sequence={sequence},office_id={office_id},description='{description}')"
            .format(**self.__dict__)
        )

    @classmethod
    def new(cls, description, office_id, sequence=0):
        return cls(
            id=None,
            sequence=sequence,
            office_id=office_id,
            description=description[:255]
        )
