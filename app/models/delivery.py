from app import db




class Delivery(db.Model):
    __tablename__ = 'deliveries'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    delivery_status = db.Column(db.String(50), default="assigned")  # assigned, on-route, delivered
    location = db.Column(db.String(200), nullable=True)  # GPS or text-based
    
    def __repr__(self):
        return f"<Delivery {self.id} - {self.delivery_status}>"