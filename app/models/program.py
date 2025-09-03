
from app import db



class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    national_alignment = db.Column(db.String(255), nullable=True)  
    focus_areas = db.Column(db.String(255), nullable=True)  
    phases = db.Column(db.String(255), nullable=True)  

    # Relationships
    projects = db.relationship("Project", back_populates="program")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'national_alignment': self.national_alignment,
            'focus_areas': self.focus_areas,
            'phases': self.phases
        }

    def __repr__(self):
        return f"<Program {self.name}>"
