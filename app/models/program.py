
from app import db
from sqlalchemy import func


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

    def __repr__(self):
        return f"<Program {self.name}>"
    
    @classmethod
    def create(cls, name, description=None, national_alignment=None, focus_areas=None, phases=None):
        """Create a new program"""
        program = cls(
            name=name,
            description=description,
            national_alignment=national_alignment,
            focus_areas=focus_areas,
            phases=phases
        )
        db.session.add(program)
        db.session.commit()
        return program

    @classmethod
    def get_by_id(cls, program_id):
        """Get program by ID"""
        return cls.query.get(program_id)

    @classmethod
    def get_by_name(cls, name):
        """Get program by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        """Get all programs"""
        return cls.query.all()

    @classmethod
    def get_by_alignment(cls, alignment):
        """Get programs by national alignment"""
        return cls.query.filter(cls.national_alignment.ilike(f'%{alignment}%')).all()

    @classmethod
    def get_by_focus_area(cls, focus_area):
        """Get programs by focus area"""
        return cls.query.filter(cls.focus_areas.ilike(f'%{focus_area}%')).all()

    def update(self, **kwargs):
        """Update program attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the program"""
        db.session.delete(self)
        db.session.commit()

    def get_projects_count(self):
        """Get total number of projects in this program"""
        return len(self.projects)

    def get_active_projects(self):
        """Get projects that are not completed"""
        from .project import Project
        return [p for p in self.projects if p.prototype_stage not in ['Completed', 'Launched']]

    def get_completed_projects(self):
        """Get completed projects"""
        from .project import Project
        return [p for p in self.projects if p.prototype_stage in ['Completed', 'Launched']]



    def get_outcomes_count(self):
        """Get total number of outcomes across all projects"""
        total = 0
        for project in self.projects:
            total += len(project.outcomes)
        return total

    def get_facilities_used(self):
        """Get list of unique facilities used by this program's projects"""
        facilities = set()
        for project in self.projects:
            if project.facility:
                facilities.add(project.facility)
        return list(facilities)

    def get_focus_areas_list(self):
        """Get focus areas as a list"""
        if self.focus_areas:
            return [area.strip() for area in self.focus_areas.split(',')]
        return []

    def get_phases_list(self):
        """Get phases as a list"""
        if self.phases:
            return [phase.strip() for phase in self.phases.split(',')]
        return []

    def get_innovation_focus_summary(self):
        """Get summary of innovation focus areas from all projects"""
        focus_areas = {}
        for project in self.projects:
            if project.innovation_focus:
                areas = [area.strip() for area in project.innovation_focus.split(',')]
                for area in areas:
                    focus_areas[area] = focus_areas.get(area, 0) + 1
        return focus_areas

    def get_commercialization_readiness(self):
        """Get commercialization readiness statistics"""
        stats = {
            'total_projects': len(self.projects),
            'with_commercialization_plan': 0,
            'prototype_stages': {}
        }
        
        for project in self.projects:
            if project.commercialization_plan:
                stats['with_commercialization_plan'] += 1
            
            stage = project.prototype_stage or 'Unknown'
            stats['prototype_stages'][stage] = stats['prototype_stages'].get(stage, 0) + 1
        
        return stats

    def to_dict(self, include_projects=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'national_alignment': self.national_alignment,
            'focus_areas': self.get_focus_areas_list(),
            'phases': self.get_phases_list(),
            'projects_count': self.get_projects_count(),
            'participants_count': self.get_participants_count(),
            'outcomes_count': self.get_outcomes_count()
        }
        
        if include_projects:
            data['projects'] = [project.to_dict() for project in self.projects]
        
        return data