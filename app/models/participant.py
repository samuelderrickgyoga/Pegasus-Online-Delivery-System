from app import db
from sqlalchemy import func

class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    affiliation = db.Column(db.String(100), nullable=True)  # CS, SE, etc.
    specialization = db.Column(db.String(100), nullable=True)  # Software, Hardware, etc.
    cross_skill_trained = db.Column(db.Boolean, default=False)
    institution = db.Column(db.String(100), nullable=True)  # SCIT, CEDAT, etc.

    # Relationships
    projects = db.relationship("ProjectParticipant", back_populates="participant")

    def __repr__(self):
        return f"<Participant {self.full_name}>"
    
    @classmethod
    def create(cls, full_name, email, affiliation=None, specialization=None, 
               cross_skill_trained=False, institution=None):
        """Create a new participant"""
        participant = cls(
            full_name=full_name,
            email=email,
            affiliation=affiliation,
            specialization=specialization,
            cross_skill_trained=cross_skill_trained,
            institution=institution
        )
        db.session.add(participant)
        db.session.commit()
        return participant

    @classmethod
    def get_by_id(cls, participant_id):
        """Get participant by ID"""
        return cls.query.get(participant_id)

    @classmethod
    def get_by_email(cls, email):
        """Get participant by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_name(cls, full_name):
        """Get participant by full name"""
        return cls.query.filter_by(full_name=full_name).first()

    @classmethod
    def get_all(cls):
        """Get all participants"""
        return cls.query.all()

    @classmethod
    def get_by_affiliation(cls, affiliation):
        """Get participants by affiliation"""
        return cls.query.filter_by(affiliation=affiliation).all()

    @classmethod
    def get_by_specialization(cls, specialization):
        """Get participants by specialization"""
        return cls.query.filter_by(specialization=specialization).all()

    @classmethod
    def get_by_institution(cls, institution):
        """Get participants by institution"""
        return cls.query.filter_by(institution=institution).all()

    @classmethod
    def get_cross_skilled(cls):
        """Get all cross-skill trained participants"""
        return cls.query.filter_by(cross_skill_trained=True).all()

    @classmethod
    def get_non_cross_skilled(cls):
        """Get participants who are not cross-skill trained"""
        return cls.query.filter_by(cross_skill_trained=False).all()

    @classmethod
    def search_participants(cls, query):
        """Search participants by name or email"""
        return cls.query.filter(
            db.or_(
                cls.full_name.ilike(f'%{query}%'),
                cls.email.ilike(f'%{query}%')
            )
        ).all()

    @classmethod
    def get_all_affiliations(cls):
        """Get all unique affiliations"""
        return [aff[0] for aff in cls.query.with_entities(cls.affiliation).distinct().all() 
                if aff[0] is not None]

    @classmethod
    def get_all_specializations(cls):
        """Get all unique specializations"""
        return [spec[0] for spec in cls.query.with_entities(cls.specialization).distinct().all() 
                if spec[0] is not None]

    @classmethod
    def get_all_institutions(cls):
        """Get all unique institutions"""
        return [inst[0] for inst in cls.query.with_entities(cls.institution).distinct().all() 
                if inst[0] is not None]

    def update(self, **kwargs):
        """Update participant attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the participant"""
        # Check if participant has associated projects
        if self.projects:
            raise ValueError("Cannot delete participant with associated projects")
        
        db.session.delete(self)
        db.session.commit()

    def get_projects_count(self):
        """Get total number of projects participant is involved in"""
        return len(self.projects)

    def get_active_projects_count(self):
        """Get number of active projects"""
        active_count = 0
        for pp in self.projects:
            if pp.project.is_active():
                active_count += 1
        return active_count

    def get_completed_projects_count(self):
        """Get number of completed projects"""
        return self.get_projects_count() - self.get_active_projects_count()

    def get_projects_list(self):
        """Get list of all projects"""
        return [pp.project for pp in self.projects]

    def get_active_projects(self):
        """Get list of active projects"""
        return [pp.project for pp in self.projects if pp.project.is_active()]

    def get_completed_projects(self):
        """Get list of completed projects"""
        return [pp.project for pp in self.projects if pp.project.is_completed()]

    def get_roles_summary(self):
        """Get summary of roles across all projects"""
        roles = {}
        for pp in self.projects:
            role = pp.role_on_project or 'Other'
            roles[role] = roles.get(role, 0) + 1
        return roles

    def get_skill_roles_summary(self):
        """Get summary of skill roles across all projects"""
        skill_roles = {}
        for pp in self.projects:
            skill_role = pp.skill_role or 'General'
            skill_roles[skill_role] = skill_roles.get(skill_role, 0) + 1
        return skill_roles

    def get_programs_involved(self):
        """Get unique programs participant is involved in"""
        programs = set()
        for pp in self.projects:
            if pp.project.program:
                programs.add(pp.project.program)
        return list(programs)

    def get_facilities_used(self):
        """Get unique facilities participant has worked in"""
        facilities = set()
        for pp in self.projects:
            if pp.project.facility:
                facilities.add(pp.project.facility)
        return list(facilities)

    def get_innovation_areas_experience(self):
        """Get innovation areas participant has experience in"""
        innovation_areas = set()
        for pp in self.projects:
            if pp.project.innovation_focus:
                areas = [area.strip() for area in pp.project.innovation_focus.split(',')]
                innovation_areas.update(areas)
        return list(innovation_areas)

    def get_outcomes_contributed(self):
        """Get outcomes from projects participant contributed to"""
        outcomes = []
        for pp in self.projects:
            outcomes.extend(pp.project.outcomes)
        return outcomes

    def get_collaboration_network(self):
        """Get other participants this person has collaborated with"""
        collaborators = set()
        for pp in self.projects:
            for other_pp in pp.project.participants:
                if other_pp.participant_id != self.id:
                    collaborators.add(other_pp.participant)
        return list(collaborators)

    def enable_cross_skill_training(self):
        """Mark participant as cross-skill trained"""
        self.cross_skill_trained = True
        db.session.commit()

    def disable_cross_skill_training(self):
        """Mark participant as not cross-skill trained"""
        self.cross_skill_trained = False
        db.session.commit()

    def is_software_specialist(self):
        """Check if participant specializes in software"""
        return self.specialization and 'software' in self.specialization.lower()

    def is_hardware_specialist(self):
        """Check if participant specializes in hardware"""
        return self.specialization and 'hardware' in self.specialization.lower()

    def has_leadership_experience(self):
        """Check if participant has leadership roles"""
        leadership_roles = ['Lead', 'Manager', 'Coordinator', 'Business Lead']
        roles = self.get_roles_summary()
        return any(role in leadership_roles for role in roles.keys())

    def get_skill_diversity_score(self):
        """Calculate skill diversity based on projects and roles"""
        score = 0
        
        # Base score for cross-skill training
        if self.cross_skill_trained:
            score += 3
        
        # Score for different skill roles
        skill_roles = len(self.get_skill_roles_summary())
        score += min(skill_roles, 3)  # Max 3 points for skill diversity
        
        # Score for different innovation areas
        innovation_areas = len(self.get_innovation_areas_experience())
        score += min(innovation_areas // 2, 2)  # Max 2 points for innovation diversity
        
        # Score for leadership
        if self.has_leadership_experience():
            score += 2
        
        return min(score, 10)  # Max score of 10

    def get_performance_metrics(self):
        """Get participant performance metrics"""
        total_projects = self.get_projects_count()
        completed_projects = self.get_completed_projects_count()
        outcomes_count = len(self.get_outcomes_contributed())
        
        return {
            'total_projects': total_projects,
            'active_projects': self.get_active_projects_count(),
            'completed_projects': completed_projects,
            'completion_rate': round((completed_projects / max(1, total_projects)) * 100, 2),
            'outcomes_contributed': outcomes_count,
            'outcomes_per_project': round(outcomes_count / max(1, total_projects), 2),
            'programs_involved': len(self.get_programs_involved()),
            'facilities_used': len(self.get_facilities_used()),
            'skill_diversity_score': self.get_skill_diversity_score(),
            'collaboration_network_size': len(self.get_collaboration_network())
        }

    def get_expertise_profile(self):
        """Get detailed expertise profile"""
        return {
            'specialization': self.specialization,
            'affiliation': self.affiliation,
            'institution': self.institution,
            'cross_skill_trained': self.cross_skill_trained,
            'innovation_areas': self.get_innovation_areas_experience(),
            'skill_roles': list(self.get_skill_roles_summary().keys()),
            'project_roles': list(self.get_roles_summary().keys()),
            'leadership_experience': self.has_leadership_experience(),
            'software_specialist': self.is_software_specialist(),
            'hardware_specialist': self.is_hardware_specialist()
        }

    def can_contribute_to_project(self, project):
        """Check if participant can contribute to a specific project"""
        if not project:
            return False, "No project provided"
        
        # Check innovation focus compatibility
        participant_areas = [area.lower() for area in self.get_innovation_areas_experience()]
        project_areas = [area.lower() for area in project.get_innovation_focus_list()]
        
        has_relevant_experience = any(
            any(p_area in proj_area or proj_area in p_area 
                for proj_area in project_areas) 
            for p_area in participant_areas
        )
        
        # Check specialization compatibility
        specialization_match = True
        if project.innovation_focus:
            project_focus = project.innovation_focus.lower()
            if 'software' in project_focus and not self.is_software_specialist():
                if not self.cross_skill_trained:
                    specialization_match = False
            elif 'hardware' in project_focus and not self.is_hardware_specialist():
                if not self.cross_skill_trained:
                    specialization_match = False
        
        if has_relevant_experience and specialization_match:
            return True, "Good match based on experience and specialization"
        elif has_relevant_experience:
            return True, "Has relevant experience in innovation area"
        elif specialization_match:
            return True, "Specialization matches project needs"
        elif self.cross_skill_trained:
            return True, "Cross-skill trained, can adapt to project needs"
        else:
            return False, "Limited compatibility with project requirements"

    def get_recommended_projects(self, available_projects):
        """Get projects recommended for this participant"""
        recommendations = []
        
        for project in available_projects:
            can_contribute, reason = self.can_contribute_to_project(project)
            if can_contribute:
                score = 0
                
                # Score based on innovation focus match
                participant_areas = [area.lower() for area in self.get_innovation_areas_experience()]
                project_areas = [area.lower() for area in project.get_innovation_focus_list()]
                
                area_matches = sum(1 for p_area in participant_areas 
                                 for proj_area in project_areas 
                                 if p_area in proj_area or proj_area in p_area)
                score += area_matches * 3
                
                # Score based on specialization match
                if project.innovation_focus:
                    project_focus = project.innovation_focus.lower()
                    if (('software' in project_focus and self.is_software_specialist()) or
                        ('hardware' in project_focus and self.is_hardware_specialist())):
                        score += 5
                
                # Bonus for cross-skill training
                if self.cross_skill_trained:
                    score += 2
                
                recommendations.append({
                    'project': project,
                    'score': score,
                    'reason': reason
                })
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations

    def get_learning_opportunities(self):
        """Identify learning opportunities for the participant"""
        opportunities = []
        
        # Cross-skill training opportunity
        if not self.cross_skill_trained:
            opportunities.append({
                'type': 'Cross-Skill Training',
                'description': 'Develop skills outside primary specialization',
                'priority': 'High'
            })
        
        # New innovation areas
        current_areas = set(area.lower() for area in self.get_innovation_areas_experience())
        emerging_areas = {'iot', 'ai', 'blockchain', 'renewable energy', 'robotics'}
        new_areas = emerging_areas - current_areas
        
        for area in new_areas:
            opportunities.append({
                'type': 'Innovation Area',
                'description': f'Gain experience in {area.upper()}',
                'priority': 'Medium'
            })
        
        # Leadership development
        if not self.has_leadership_experience():
            opportunities.append({
                'type': 'Leadership Development',
                'description': 'Take on leadership roles in projects',
                'priority': 'Medium'
            })
        
        return opportunities

    def to_dict(self, include_projects=False, include_metrics=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'affiliation': self.affiliation,
            'specialization': self.specialization,
            'cross_skill_trained': self.cross_skill_trained,
            'institution': self.institution,
            'projects_count': self.get_projects_count(),
            'active_projects_count': self.get_active_projects_count(),
            'completed_projects_count': self.get_completed_projects_count()
        }
        
        if include_metrics:
            data.update({
                'performance_metrics': self.get_performance_metrics(),
                'expertise_profile': self.get_expertise_profile(),
                'innovation_areas': self.get_innovation_areas_experience(),
                'collaboration_network_size': len(self.get_collaboration_network()),
                'learning_opportunities': self.get_learning_opportunities()
            })
        
        if include_projects:
            data.update({
                'active_projects': [p.to_dict() for p in self.get_active_projects()],
                'completed_projects': [p.to_dict() for p in self.get_completed_projects()],
                'roles_summary': self.get_roles_summary(),
                'skill_roles_summary': self.get_skill_roles_summary(),
                'programs_involved': [p.to_dict() for p in self.get_programs_involved()],
                'facilities_used': [f.to_dict() for f in self.get_facilities_used()]
            })
        
        return data