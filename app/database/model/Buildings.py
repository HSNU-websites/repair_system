from .common import db


class Buildings(db.Model):
    """
    Buildings.id = 1 will be default building
    """

    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Buildings.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Buildings(id={id},sequence={sequence},description='{description}')".format(**self.__dict__)
