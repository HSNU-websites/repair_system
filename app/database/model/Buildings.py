from .common import db


class Buildings(db.Model):
    """
    Buildings.id = 1 will be default building
    """

    __tablename__ = "buildings"
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
        return "Buildings(id={id},sequence={sequence},description='{description}')".format(**self.__dict__)
