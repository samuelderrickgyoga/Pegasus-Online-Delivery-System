from app import db



class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100), nullable=True)
    
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name} (${self.price})>"