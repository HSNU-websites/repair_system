from .common import db

class Offices(db.Model):
    """
    The table manifests what the office should be responsible for the broken items.
    """

    __tablename__ = "offices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    item = db.relationship("Items", backref="office")

    def __init__(self, description):
        self.description = description