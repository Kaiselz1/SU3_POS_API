from app import db

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(200))
    phone = db.Column(db.String(50))

    users = db.relationship('User', backref='branch', lazy=True)