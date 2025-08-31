
from app import db



class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    role = db.Column(db.String(50), nullable=False)  # customer, admin, delivery
    
    orders = db.relationship('Order', backref='customer', lazy=True)
    deliveries = db.relationship('Delivery', backref='delivery_person', lazy=True)

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"