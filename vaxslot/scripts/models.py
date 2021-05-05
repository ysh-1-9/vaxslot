from vaxslot import db

class Data(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), primary_key=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=True)

    def _repr_(self) -> str:
        return f"E-Mail - {self.email} Age - {self.age} State - {self.district}"
