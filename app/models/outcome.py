from app import db
from datetime import datetime

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
    
    
    @classmethod
    def create(cls, project_id, title, description=None, artifact_link=None, 
               outcome_type=None, quality_certification=None, commercialization_status=None):
        """Create a new outcome"""
        outcome = cls(
            project_id=project_id,
            title=title,
            description=description,
            artifact_link=artifact_link,
            outcome_type=outcome_type,
            quality_certification=quality_certification,
            commercialization_status=commercialization_status
        )
        db.session.add(outcome)
        db.session.commit()
        return outcome

    @classmethod
    def get_by_id(cls, outcome_id):
        """Get outcome by ID"""
        return cls.query.get(outcome_id)

    @classmethod
    def get_by_title(cls, title):
        """Get outcome by title"""
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_all(cls):
        """Get all outcomes"""
        return cls.query.all()

    @classmethod
    def get_by_project(cls, project_id):
        """Get all outcomes for a specific project"""
        return cls.query.filter_by(project_id=project_id).all()

    @classmethod
    def get_by_type(cls, outcome_type):
        """Get outcomes by type"""
        return cls.query.filter_by(outcome_type=outcome_type).all()

    @classmethod
    def get_certified_outcomes(cls):
        """Get outcomes with quality certification"""
        return cls.query.filter(cls.quality_certification.isnot(None)).all()

    @classmethod
    def get_commercialized_outcomes(cls):
        """Get outcomes that have been commercialized"""
        return cls.query.filter(
            cls.commercialization_status.in_(['Demoed', 'Launched', 'In Market'])
        ).all()

    @classmethod
    def get_by_commercialization_status(cls, status):
        """Get outcomes by commercialization status"""
        return cls.query.filter_by(commercialization_status=status).all()

    @classmethod
    def search_outcomes(cls, query):
        """Search outcomes by title or description"""
        return cls.query.filter(
            db.or_(
                cls.title.ilike(f'%{query}%'),
                cls.description.ilike(f'%{query}%')
            )
        ).all()

    @classmethod
    def get_all_types(cls):
        """Get all unique outcome types"""
        return [otype[0] for otype in cls.query.with_entities(cls.outcome_type).distinct().all() 
                if otype[0] is not None]

    @classmethod
    def get_all_commercialization_statuses(cls):
        """Get all unique commercialization statuses"""
        return [status[0] for status in cls.query.with_entities(cls.commercialization_status).distinct().all() 
                if status[0] is not None]

    def update(self, **kwargs):
        """Update outcome attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the outcome"""
        db.session.delete(self)
        db.session.commit()

    def get_project_title(self):
        """Get the title of the associated project"""
        return self.project.title if self.project else None

    def get_project_program(self):
        """Get the program of the associated project"""
        return self.project.program if self.project else None

    def get_project_facility(self):
        """Get the facility of the associated project"""
        return self.project.facility if self.project else None

    def has_artifact_link(self):
        """Check if outcome has an artifact link"""
        return bool(self.artifact_link and self.artifact_link.strip())

    def is_certified(self):
        """Check if outcome has quality certification"""
        return bool(self.quality_certification and self.quality_certification.strip())

    def is_commercialized(self):
        """Check if outcome has been commercialized"""
        commercial_statuses = ['Demoed', 'Launched', 'In Market']
        return self.commercialization_status in commercial_statuses

    def is_launched(self):
        """Check if outcome has been launched to market"""
        return self.commercialization_status in ['Launched', 'In Market']

    def is_prototype(self):
        """Check if outcome is a prototype"""
        return self.outcome_type and 'prototype' in self.outcome_type.lower()

    def is_design_artifact(self):
        """Check if outcome is a design artifact (CAD, PCB, etc.)"""
        design_types = ['CAD', 'PCB', 'Schematic', 'Design']
        return any(dtype.lower() in (self.outcome_type or '').lower() 
                  for dtype in design_types)

    def is_documentation(self):
        """Check if outcome is documentation"""
        doc_types = ['Report', 'Documentation', 'Manual', 'Guide']
        return any(dtype.lower() in (self.outcome_type or '').lower() 
                  for dtype in doc_types)

    def get_outcome_maturity_level(self):
        """Calculate outcome maturity level"""
        maturity_score = 0
        max_score = 10
        
        # Basic outcome info (2 points)
        if self.description:
            maturity_score += 1
        if self.has_artifact_link():
            maturity_score += 1
        
        # Outcome type specificity (2 points)
        if self.outcome_type:
            maturity_score += 2
        
        # Quality certification (3 points)
        if self.is_certified():
            maturity_score += 3
        
        # Commercialization progress (3 points)
        if self.commercialization_status:
            if self.commercialization_status == 'Planned':
                maturity_score += 1
            elif self.commercialization_status == 'In Development':
                maturity_score += 1
            elif self.commercialization_status == 'Demoed':
                maturity_score += 2
            elif self.commercialization_status in ['Launched', 'In Market']:
                maturity_score += 3
        
        return round((maturity_score / max_score) * 100, 2)

    def get_innovation_impact_score(self):
        """Calculate innovation impact based on outcome characteristics"""
        impact_score = 0
        
        # Base score for prototype or physical outcome
        if self.is_prototype():
            impact_score += 3
        elif self.is_design_artifact():
            impact_score += 2
        elif self.is_documentation():
            impact_score += 1
        
        # Certification bonus
        if self.is_certified():
            impact_score += 2
        
        # Commercialization bonus
        if self.is_launched():
            impact_score += 4
        elif self.commercialization_status == 'Demoed':
            impact_score += 2
        
        # Innovation focus alignment (from project)
        if self.project and self.project.innovation_focus:
            high_impact_areas = ['iot', 'ai', 'renewable', 'automation', 'robotics']
            project_focus = self.project.innovation_focus.lower()
            if any(area in project_focus for area in high_impact_areas):
                impact_score += 2
        
        return min(impact_score, 10)  # Cap at 10

    def get_related_outcomes(self):
        """Get other outcomes from the same project"""
        if not self.project:
            return []
        
        return [outcome for outcome in self.project.outcomes 
                if outcome.id != self.id]

    def get_similar_outcomes_across_projects(self):
        """Get similar outcomes from other projects (same type)"""
        if not self.outcome_type:
            return []
        
        return Outcome.query.filter(
            Outcome.outcome_type == self.outcome_type,
            Outcome.id != self.id
        ).all()

    def get_certification_details(self):
        """Get detailed certification information"""
        if not self.is_certified():
            return None
        
        return {
            'certification': self.quality_certification,
            'certified': True,
            'certification_impact': 'High' if 'UIRI' in self.quality_certification else 'Medium'
        }

    def get_commercialization_potential(self):
        """Assess commercialization potential"""
        potential_score = 0
        potential_factors = []
        
        # Current status
        if self.is_launched():
            return {
                'score': 10,
                'status': 'Already Commercialized',
                'factors': ['Product is in market']
            }
        
        # Prototype readiness
        if self.is_prototype():
            potential_score += 3
            potential_factors.append('Physical prototype exists')
        
        # Certification
        if self.is_certified():
            potential_score += 3
            potential_factors.append('Quality certified')
        
        # Project commercialization plan
        if self.project and self.project.has_commercialization_plan():
            potential_score += 2
            potential_factors.append('Commercialization plan exists')
        
        # Innovation focus
        if self.project and self.project.innovation_focus:
            marketable_areas = ['iot', 'renewable', 'automation', 'medical']
            if any(area in self.project.innovation_focus.lower() for area in marketable_areas):
                potential_score += 2
                potential_factors.append('Market-relevant innovation area')
        
        return {
            'score': min(potential_score, 10),
            'status': self.commercialization_status or 'Not Started',
            'factors': potential_factors
        }

    def get_outcome_metrics(self):
        """Get comprehensive outcome metrics"""
        return {
            'maturity_level': self.get_outcome_maturity_level(),
            'innovation_impact': self.get_innovation_impact_score(),
            'commercialization_potential': self.get_commercialization_potential(),
            'certification_details': self.get_certification_details(),
            'has_artifact': self.has_artifact_link(),
            'is_prototype': self.is_prototype(),
            'is_design_artifact': self.is_design_artifact(),
            'is_documentation': self.is_documentation(),
            'related_outcomes_count': len(self.get_related_outcomes())
        }

    def get_value_proposition(self):
        """Generate value proposition for the outcome"""
        if not self.project:
            return "Outcome value not determined"
        
        value_points = []
        
        # Innovation focus value
        if self.project.innovation_focus:
            focus_areas = self.project.innovation_focus
            value_points.append(f"Advances {focus_areas} technology")
        
        # Certification value
        if self.is_certified():
            value_points.append(f"Quality certified by {self.quality_certification}")
        
        # Commercialization value
        if self.is_launched():
            value_points.append("Market-proven solution")
        elif self.commercialization_status == 'Demoed':
            value_points.append("Demonstrated market readiness")
        
        # Technical value
        if self.is_prototype():
            value_points.append("Functional prototype ready for testing")
        elif self.is_design_artifact():
            value_points.append("Complete technical specifications available")
        
        return "; ".join(value_points) if value_points else "Innovative solution with potential applications"

    def to_dict(self, include_project_info=False, include_metrics=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'artifact_link': self.artifact_link,
            'outcome_type': self.outcome_type,
            'quality_certification': self.quality_certification,
            'commercialization_status': self.commercialization_status,
            'is_certified': self.is_certified(),
            'is_commercialized': self.is_commercialized(),
            'is_launched': self.is_launched(),
            'has_artifact_link': self.has_artifact_link()
        }
        
        if include_project_info and self.project:
            data.update({
                'project_title': self.project.title,
                'project_program': self.project.program.name if self.project.program else None,
                'project_facility': self.project.facility.name if self.project.facility else None,
                'project_innovation_focus': self.project.innovation_focus,
                'project_stage': self.project.prototype_stage
            })
        
        if include_metrics:
            data.update({
                'outcome_metrics': self.get_outcome_metrics(),
                'value_proposition': self.get_value_proposition(),
                'related_outcomes_count': len(self.get_related_outcomes()),
                'similar_outcomes_count': len(self.get_similar_outcomes_across_projects())
            })
        
        return data