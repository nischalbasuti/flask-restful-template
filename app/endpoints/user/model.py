from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Serialize object.
    def to_dict(self):
        ret = {c.name: getattr(self, c.name) for c in  self.__table__.columns}
        return ret

    def __str__(self):
        return str(self.to_dict())
