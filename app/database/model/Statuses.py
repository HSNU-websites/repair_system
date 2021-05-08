from .common import db

class Statuses(db.Model):
    """
    Statuses.id = 1 will be default item
    """

    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, sequence=None, **kwargs):
        if sequence is None:
            if s := db.session.query(db.func.max(Statuses.sequence)).first()[0]:
                self.sequence = s + 1
            else:
                self.sequence = 1
        else:
            self.sequence = sequence
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]

    def __repr__(self):
        return "Statuses(id={id}, sequence={sequence}, description='{description}')".format(**self.__dict__)
