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

    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'name': self.name,
            'capabilities': self.capabilities,
            'description': self.description,
            'inventory_code': self.inventory_code,
            'usage_domain': self.usage_domain,
            'support_phase': self.support_phase
        }

    def __repr__(self):
        return f"<Equipment {self.name}>"