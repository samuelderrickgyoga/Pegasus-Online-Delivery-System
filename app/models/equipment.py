from app import db



class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    capabilities = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    inventory_code = db.Column(db.String(100), nullable=True)
    usage_domain = db.Column(db.String(100), nullable=True)  # Electronics, Mechanical, IoT
    support_phase = db.Column(db.String(100), nullable=True)  # Training, Prototyping, etc.

    # Relationships
    facility = db.relationship("Facility", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment {self.name}>"