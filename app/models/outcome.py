from app import db


class Outcome(db.Model):
    __tablename__ = "outcomes"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    artifact_link = db.Column(db.String(255), nullable=True)
    outcome_type = db.Column(db.String(100), nullable=True)  # CAD, PCB, Prototype, Report
    quality_certification = db.Column(db.String(255), nullable=True)  # UIRI certification, etc.
    commercialization_status = db.Column(db.String(100), nullable=True)  # Demoed, Launched, etc.

    # Relationships
    project = db.relationship("Project", back_populates="outcomes")

    def __repr__(self):
        return f"<Outcome {self.title}>"