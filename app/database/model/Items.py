from .common import db


class Items(db.Model):
    """
    Items.id = 1 will be default item.

    id: PK.
    sequence: The displayed order.
    description: The name of the item.
    """

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    office_id = db.Column(db.ForeignKey("offices.id"), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, office_id, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Items.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
            # flush
        else:
            self.sequence = sequence
        self.office_id = office_id
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Items(id={id},sequence={sequence},description='{description}')".format(
            **self.__dict__
        )
