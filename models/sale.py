from app import db

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String(200))

    items = db.relationship('SaleItem', backref='sale', lazy=True)