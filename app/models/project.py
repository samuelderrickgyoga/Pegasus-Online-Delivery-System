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

    def __repr__(self):
        return f"<Project {self.title}>"