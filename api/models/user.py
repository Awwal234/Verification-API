from ..utils import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        return f"SignUp('{self.full_name}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
