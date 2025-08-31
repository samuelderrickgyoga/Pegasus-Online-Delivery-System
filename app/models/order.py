from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, in-progress, delivered, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    delivery = db.relationship('Delivery', uselist=False, backref='order')

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"