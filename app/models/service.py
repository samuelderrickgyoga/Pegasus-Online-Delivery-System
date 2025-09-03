from app import db




class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True) 
    skill_type = db.Column(db.String(100), nullable=True)  

    # Relationships
    facility = db.relationship("Facility", back_populates="services")

    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'skill_type': self.skill_type
        }

    def __repr__(self):
        return f"<Service {self.name}>"
