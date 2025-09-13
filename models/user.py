from app import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile = db.Column(db.String(200))

    sales = db.relationship('Sale', backref='user', lazy=True)