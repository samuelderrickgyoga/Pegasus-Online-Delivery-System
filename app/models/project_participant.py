from app import db

class ProjectParticipant(db.Model):
    __tablename__ = "project_participants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    role_on_project = db.Column(db.String(50), nullable=False)  # Student, Lecturer, Contributor
    skill_role = db.Column(db.String(50), nullable=True)  # Developer, Engineer, Designer, Business Lead

    # Relationships
    project = db.relationship("Project", back_populates="participants")
    participant = db.relationship("Participant", back_populates="projects")

    def __repr__(self):
        return f"<ProjectParticipant project_id={self.project_id}, participant_id={self.participant_id}, role={self.role_on_project}, skill={self.skill_role}>"
