from app import db



class Facility(db.Model):
    __tablename__ = "facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    partner_org = db.Column(db.String(255), nullable=True)
    facility_type = db.Column(db.String(100), nullable=True) 
    capabilities = db.Column(db.String(255), nullable=True)  

    # Relationships
    services = db.relationship("Service", back_populates="facility")
    equipment = db.relationship("Equipment", back_populates="facility")
    projects = db.relationship("Project", back_populates="facility")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'partner_organization': self.partner_org,
            'facility_type': self.facility_type,
            'capabilities': self.capabilities
        }

    def __repr__(self):
        return f"<Facility {self.name}>"
