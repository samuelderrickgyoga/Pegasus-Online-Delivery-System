from app import db
from sqlalchemy import func
from datetime import datetime


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
    
    
    @classmethod
    def create(cls, program_id, facility_id, title, nature=None, description=None, 
               innovation_focus=None, prototype_stage=None, testing_requirements=None, 
               commercialization_plan=None):
        """Create a new project"""
        project = cls(
            program_id=program_id,
            facility_id=facility_id,
            title=title,
            nature=nature,
            description=description,
            innovation_focus=innovation_focus,
            prototype_stage=prototype_stage,
            testing_requirements=testing_requirements,
            commercialization_plan=commercialization_plan
        )
        db.session.add(project)
        db.session.commit()
        return project

    @classmethod
    def get_by_id(cls, project_id):
        """Get project by ID"""
        return cls.query.get(project_id)

    @classmethod
    def get_by_title(cls, title):
        """Get project by title"""
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_all(cls):
        """Get all projects"""
        return cls.query.all()

    @classmethod
    def get_by_program(cls, program_id):
        """Get all projects for a specific program"""
        return cls.query.filter_by(program_id=program_id).all()

    @classmethod
    def get_by_facility(cls, facility_id):
        """Get all projects at a specific facility"""
        return cls.query.filter_by(facility_id=facility_id).all()

    @classmethod
    def get_by_nature(cls, nature):
        """Get projects by nature (research, prototype, applied)"""
        return cls.query.filter_by(nature=nature).all()

    @classmethod
    def get_by_stage(cls, stage):
        """Get projects by prototype stage"""
        return cls.query.filter_by(prototype_stage=stage).all()

    @classmethod
    def get_active_projects(cls):
        """Get projects that are not completed"""
        return cls.query.filter(
            ~cls.prototype_stage.in_(['Completed', 'Launched'])
        ).all()

    @classmethod
    def get_completed_projects(cls):
        """Get completed projects"""
        return cls.query.filter(
            cls.prototype_stage.in_(['Completed', 'Launched'])
        ).all()

    @classmethod
    def search_by_innovation_focus(cls, focus_area):
        """Search projects by innovation focus"""
        return cls.query.filter(cls.innovation_focus.ilike(f'%{focus_area}%')).all()

    @classmethod
    def search_projects(cls, query):
        """Search projects by title, description, or innovation focus"""
        return cls.query.filter(
            db.or_(
                cls.title.ilike(f'%{query}%'),
                cls.description.ilike(f'%{query}%'),
                cls.innovation_focus.ilike(f'%{query}%')
            )
        ).all()

    def update(self, **kwargs):
        """Update project attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the project"""
        db.session.delete(self)
        db.session.commit()

    def get_innovation_focus_list(self):
        """Get innovation focus areas as a list"""
        if self.innovation_focus:
            return [focus.strip() for focus in self.innovation_focus.split(',')]
        return []

    def add_innovation_focus(self, focus_area):
        """Add a new innovation focus area"""
        current_focus = self.get_innovation_focus_list()
        if focus_area not in current_focus:
            current_focus.append(focus_area)
            self.innovation_focus = ', '.join(current_focus)
            db.session.commit()

    def remove_innovation_focus(self, focus_area):
        """Remove an innovation focus area"""
        current_focus = self.get_innovation_focus_list()
        if focus_area in current_focus:
            current_focus.remove(focus_area)
            self.innovation_focus = ', '.join(current_focus) if current_focus else None
            db.session.commit()

    def get_participants_count(self):
        """Get total number of participants"""
        return len(self.participants)

    def get_outcomes_count(self):
        """Get total number of outcomes"""
        return len(self.outcomes)

    def get_program_name(self):
        """Get the program name"""
        return self.program.name if self.program else None

    def get_facility_name(self):
        """Get the facility name"""
        return self.facility.name if self.facility else None

    def get_facility_location(self):
        """Get the facility location"""
        return self.facility.location if self.facility else None

    def is_active(self):
        """Check if project is active (not completed or launched)"""
        return self.prototype_stage not in ['Completed', 'Launched']

    def is_completed(self):
        """Check if project is completed"""
        return self.prototype_stage in ['Completed', 'Launched']

    def has_commercialization_plan(self):
        """Check if project has a commercialization plan"""
        return bool(self.commercialization_plan and self.commercialization_plan.strip())

    def has_testing_requirements(self):
        """Check if project has testing requirements defined"""
        return bool(self.testing_requirements and self.testing_requirements.strip())

    def get_project_maturity_score(self):
        """Calculate project maturity score based on various factors"""
        score = 0
        max_score = 10
        
        # Basic project info (2 points)
        if self.description:
            score += 1
        if self.innovation_focus:
            score += 1
            
        # Stage progression (3 points)
        stage_scores = {
            'Concept': 1,
            'Design': 2,
            'MVP': 3,
            'Testing': 3,
            'Completed': 3,
            'Launched': 3
        }
        score += stage_scores.get(self.prototype_stage, 0)
        
        # Requirements and planning (3 points)
        if self.has_testing_requirements():
            score += 1
        if self.has_commercialization_plan():
            score += 2
            
        # Participation and outcomes (2 points)
        if self.get_participants_count() > 0:
            score += 1
        if self.get_outcomes_count() > 0:
            score += 1
            
        return round((score / max_score) * 100, 2)

    def get_participants_by_role(self):
        """Get participants grouped by their role"""
        participants_by_role = {}
        for pp in self.participants:
            role = pp.role_on_project or 'Other'
            if role not in participants_by_role:
                participants_by_role[role] = []
            participants_by_role[role].append(pp.participant)
        return participants_by_role

    def get_participants_by_skill(self):
        """Get participants grouped by their skill role"""
        participants_by_skill = {}
        for pp in self.participants:
            skill = pp.skill_role or 'General'
            if skill not in participants_by_skill:
                participants_by_skill[skill] = []
            participants_by_skill[skill].append(pp.participant)
        return participants_by_skill

    def get_cross_skilled_participants(self):
        """Get participants who are cross-skill trained"""
        cross_skilled = []
        for pp in self.participants:
            if pp.participant.cross_skill_trained:
                cross_skilled.append(pp.participant)
        return cross_skilled

    def get_outcomes_by_type(self):
        """Get outcomes grouped by type"""
        outcomes_by_type = {}
        for outcome in self.outcomes:
            outcome_type = outcome.outcome_type or 'Other'
            if outcome_type not in outcomes_by_type:
                outcomes_by_type[outcome_type] = []
            outcomes_by_type[outcome_type].append(outcome)
        return outcomes_by_type

    def get_certified_outcomes(self):
        """Get outcomes with quality certification"""
        return [outcome for outcome in self.outcomes 
                if outcome.quality_certification]

    def get_commercialized_outcomes(self):
        """Get outcomes that have been commercialized"""
        return [outcome for outcome in self.outcomes 
                if outcome.commercialization_status in ['Demoed', 'Launched']]

    def get_required_facility_capabilities(self):
        """Get facility capabilities required for this project"""
        required_caps = []
        
        # Extract from innovation focus
        if self.innovation_focus:
            focus_areas = self.get_innovation_focus_list()
            for area in focus_areas:
                if 'iot' in area.lower():
                    required_caps.extend(['Electronics', 'Programming', 'Sensors'])
                elif 'renewable' in area.lower():
                    required_caps.extend(['Electronics', 'Power Systems', 'Testing'])
                elif 'automation' in area.lower():
                    required_caps.extend(['Mechanical', 'Programming', 'Control Systems'])
        
        # Extract from testing requirements
        if self.testing_requirements:
            testing_text = self.testing_requirements.lower()
            if 'pcb' in testing_text:
                required_caps.append('PCB Testing')
            if 'mechanical' in testing_text:
                required_caps.append('Mechanical Testing')
            if 'performance' in testing_text:
                required_caps.append('Performance Testing')
        
        return list(set(required_caps))  # Remove duplicates

    def check_facility_compatibility(self):
        """Check if assigned facility can support project requirements"""
        if not self.facility:
            return {'compatible': False, 'reason': 'No facility assigned'}
        
        required_caps = self.get_required_facility_capabilities()
        if not required_caps:
            return {'compatible': True, 'reason': 'No specific requirements'}
        
        facility_caps = self.facility.get_capabilities_list()
        missing_caps = [cap for cap in required_caps 
                       if not any(cap.lower() in fc.lower() for fc in facility_caps)]
        
        if missing_caps:
            return {
                'compatible': False, 
                'reason': f'Missing capabilities: {", ".join(missing_caps)}',
                'missing_capabilities': missing_caps
            }
        
        return {'compatible': True, 'reason': 'All requirements met'}

    def get_project_timeline_estimate(self):
        """Estimate project timeline based on stage and complexity"""
        stage_durations = {
            'Concept': {'min': 2, 'max': 4},  # weeks
            'Design': {'min': 4, 'max': 8},
            'MVP': {'min': 6, 'max': 12},
            'Testing': {'min': 2, 'max': 6},
            'Completed': {'min': 0, 'max': 0},
            'Launched': {'min': 0, 'max': 0}
        }
        
        current_stage = self.prototype_stage or 'Concept'
        base_duration = stage_durations.get(current_stage, {'min': 4, 'max': 8})
        
        # Adjust based on complexity factors
        complexity_factor = 1.0
        
        if len(self.get_innovation_focus_list()) > 2:
            complexity_factor += 0.3
        
        if self.has_testing_requirements():
            complexity_factor += 0.2
            
        if self.get_participants_count() > 5:
            complexity_factor += 0.1  # More coordination needed
        
        return {
            'stage': current_stage,
            'estimated_min_weeks': int(base_duration['min'] * complexity_factor),
            'estimated_max_weeks': int(base_duration['max'] * complexity_factor),
            'complexity_factor': round(complexity_factor, 2)
        }

    def to_dict(self, include_relationships=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'program_id': self.program_id,
            'facility_id': self.facility_id,
            'title': self.title,
            'nature': self.nature,
            'description': self.description,
            'innovation_focus': self.get_innovation_focus_list(),
            'prototype_stage': self.prototype_stage,
            'testing_requirements': self.testing_requirements,
            'commercialization_plan': self.commercialization_plan,
            'participants_count': self.get_participants_count(),
            'outcomes_count': self.get_outcomes_count(),
            'maturity_score': self.get_project_maturity_score(),
            'is_active': self.is_active(),
            'has_commercialization_plan': self.has_commercialization_plan()
        }
        
        if include_relationships:
            data.update({
                'program_name': self.get_program_name(),
                'facility_name': self.get_facility_name(),
                'facility_location': self.get_facility_location(),
                'participants_by_role': {role: [p.to_dict() for p in participants] 
                                       for role, participants in self.get_participants_by_role().items()},
                'outcomes_by_type': {otype: [o.to_dict() for o in outcomes] 
                                   for otype, outcomes in self.get_outcomes_by_type().items()},
                'facility_compatibility': self.check_facility_compatibility(),
                'timeline_estimate': self.get_project_timeline_estimate(),
                'required_capabilities': self.get_required_facility_capabilities()
            })
        
        return data