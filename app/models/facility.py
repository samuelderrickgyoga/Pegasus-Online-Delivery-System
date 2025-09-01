from app import db
from sqlalchemy import func


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

    def __repr__(self):
        return f"<Facility {self.name}>"
    
    @classmethod
    def create(cls, name, location=None, description=None, partner_org=None, 
               facility_type=None, capabilities=None):
        """Create a new facility"""
        facility = cls(
            name=name,
            location=location,
            description=description,
            partner_org=partner_org,
            facility_type=facility_type,
            capabilities=capabilities
        )
        db.session.add(facility)
        db.session.commit()
        return facility

    @classmethod
    def get_by_id(cls, facility_id):
        """Get facility by ID"""
        return cls.query.get(facility_id)

    @classmethod
    def get_by_name(cls, name):
        """Get facility by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        """Get all facilities"""
        return cls.query.all()

    @classmethod
    def get_by_type(cls, facility_type):
        """Get facilities by type"""
        return cls.query.filter_by(facility_type=facility_type).all()

    @classmethod
    def get_by_partner(cls, partner_org):
        """Get facilities by partner organization"""
        return cls.query.filter_by(partner_org=partner_org).all()

    @classmethod
    def get_by_location(cls, location):
        """Get facilities by location"""
        return cls.query.filter(cls.location.ilike(f'%{location}%')).all()

    @classmethod
    def search_by_capability(cls, capability):
        """Search facilities by capability"""
        return cls.query.filter(cls.capabilities.ilike(f'%{capability}%')).all()

    def update(self, **kwargs):
        """Update facility attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the facility"""
        # Check if facility has associated projects
        if self.projects:
            raise ValueError("Cannot delete facility with associated projects")
        
        db.session.delete(self)
        db.session.commit()

    def get_capabilities_list(self):
        """Get capabilities as a list"""
        if self.capabilities:
            return [cap.strip() for cap in self.capabilities.split(',')]
        return []

    def add_capability(self, capability):
        """Add a new capability to the facility"""
        current_caps = self.get_capabilities_list()
        if capability not in current_caps:
            current_caps.append(capability)
            self.capabilities = ', '.join(current_caps)
            db.session.commit()

    def remove_capability(self, capability):
        """Remove a capability from the facility"""
        current_caps = self.get_capabilities_list()
        if capability in current_caps:
            current_caps.remove(capability)
            self.capabilities = ', '.join(current_caps) if current_caps else None
            db.session.commit()

    def get_services_count(self):
        """Get total number of services offered"""
        return len(self.services)

    def get_equipment_count(self):
        """Get total number of equipment items"""
        return len(self.equipment)

    def get_projects_count(self):
        """Get total number of projects using this facility"""
        return len(self.projects)

    def get_active_projects_count(self):
        """Get number of active projects"""
        return len([p for p in self.projects 
                   if p.prototype_stage not in ['Completed', 'Launched']])

    def get_services_by_category(self):
        """Get services grouped by category"""
        services_by_cat = {}
        for service in self.services:
            category = service.category or 'Other'
            if category not in services_by_cat:
                services_by_cat[category] = []
            services_by_cat[category].append(service)
        return services_by_cat

    def get_equipment_by_domain(self):
        """Get equipment grouped by usage domain"""
        equipment_by_domain = {}
        for equipment in self.equipment:
            domain = equipment.usage_domain or 'General'
            if domain not in equipment_by_domain:
                equipment_by_domain[domain] = []
            equipment_by_domain[domain].append(equipment)
        return equipment_by_domain

    def get_utilization_stats(self):
        """Get facility utilization statistics"""
        total_projects = len(self.projects)
        active_projects = self.get_active_projects_count()
        completed_projects = total_projects - active_projects
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'services_offered': len(self.services),
            'equipment_available': len(self.equipment),
            'utilization_rate': round((active_projects / max(1, total_projects)) * 100, 2)
        }

    def get_innovation_areas(self):
        """Get unique innovation focus areas from projects"""
        innovation_areas = set()
        for project in self.projects:
            if project.innovation_focus:
                areas = [area.strip() for area in project.innovation_focus.split(',')]
                innovation_areas.update(areas)
        return list(innovation_areas)

    def has_capability(self, capability):
        """Check if facility has a specific capability"""
        return capability.lower() in [cap.lower() for cap in self.get_capabilities_list()]

    def can_support_project_needs(self, required_capabilities):
        """Check if facility can support project with given requirements"""
        facility_caps = [cap.lower() for cap in self.get_capabilities_list()]
        required_caps = [cap.lower() for cap in required_capabilities]
        return all(req_cap in facility_caps for req_cap in required_caps)

    def get_partner_collaboration_stats(self):
        """Get statistics about partner collaborations"""
        if not self.partner_org:
            return None
        
        return {
            'partner_organization': self.partner_org,
            'total_projects': len(self.projects),
            'services_provided': len(self.services),
            'equipment_shared': len(self.equipment),
            'innovation_areas_supported': len(self.get_innovation_areas())
        }

    def to_dict(self, include_related=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'partner_org': self.partner_org,
            'facility_type': self.facility_type,
            'capabilities': self.get_capabilities_list(),
            'services_count': self.get_services_count(),
            'equipment_count': self.get_equipment_count(),
            'projects_count': self.get_projects_count(),
            'active_projects_count': self.get_active_projects_count()
        }
        
        if include_related:
            data.update({
                'services': [service.to_dict() for service in self.services],
                'equipment': [equip.to_dict() for equip in self.equipment],
                'utilization_stats': self.get_utilization_stats(),
                'innovation_areas': self.get_innovation_areas()
            })
        
        return data