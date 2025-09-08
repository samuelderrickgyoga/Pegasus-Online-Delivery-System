from app import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    nature = db.Column(db.String(100), nullable=True)  
    description = db.Column(db.Text, nullable=True)
    innovation_focus = db.Column(db.String(255), nullable=True) 
    prototype_stage = db.Column(db.String(100), nullable=True)  
    testing_requirements = db.Column(db.Text, nullable=True)
    commercialization_plan = db.Column(db.Text, nullable=True)

    # Relationships
    program = db.relationship("Program", back_populates="projects")
    facility = db.relationship("Facility", back_populates="projects")
    participants = db.relationship("ProjectParticipant", back_populates="project")
    outcomes = db.relationship("Outcome", back_populates="project")

    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'facility_id': self.facility_id,
            'title': self.title,
            'nature': self.nature,
            'description': self.description,
            'innovation_focus': self.innovation_focus,
            'prototype_stage': self.prototype_stage,
            'testing_requirements': self.testing_requirements,
            'commercialization_plan': self.commercialization_plan
        }

    def __repr__(self):
        return f"<Project {self.title}>"