from app import db




class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True) 
    skill_type = db.Column(db.String(100), nullable=True)  

    # Relationships
    facility = db.relationship("Facility", back_populates="services")

    def __repr__(self):
        return f"<Service {self.name}>"

    @classmethod
    def create(cls, facility_id, name, description=None, category=None, skill_type=None):
        """Create a new service"""
        service = cls(
            facility_id=facility_id,
            name=name,
            description=description,
            category=category,
            skill_type=skill_type
        )
        db.session.add(service)
        db.session.commit()
        return service

    @classmethod
    def get_by_id(cls, service_id):
        """Get service by ID"""
        return cls.query.get(service_id)

    @classmethod
    def get_by_name(cls, name):
        """Get service by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        """Get all services"""
        return cls.query.all()

    @classmethod
    def get_by_facility(cls, facility_id):
        """Get all services for a specific facility"""
        return cls.query.filter_by(facility_id=facility_id).all()

    @classmethod
    def get_by_category(cls, category):
        """Get services by category"""
        return cls.query.filter_by(category=category).all()

    @classmethod
    def get_by_skill_type(cls, skill_type):
        """Get services by skill type"""
        return cls.query.filter_by(skill_type=skill_type).all()

    @classmethod
    def search_services(cls, query):
        """Search services by name or description"""
        return cls.query.filter(
            db.or_(
                cls.name.ilike(f'%{query}%'),
                cls.description.ilike(f'%{query}%')
            )
        ).all()

    @classmethod
    def get_all_categories(cls):
        """Get all unique service categories"""
        return [cat[0] for cat in cls.query.with_entities(cls.category).distinct().all() 
                if cat[0] is not None]

    @classmethod
    def get_all_skill_types(cls):
        """Get all unique skill types"""
        return [skill[0] for skill in cls.query.with_entities(cls.skill_type).distinct().all() 
                if skill[0] is not None]

    def update(self, **kwargs):
        """Update service attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the service"""
        db.session.delete(self)
        db.session.commit()

    def get_facility_name(self):
        """Get the name of the facility providing this service"""
        return self.facility.name if self.facility else None

    def get_facility_location(self):
        """Get the location of the facility providing this service"""
        return self.facility.location if self.facility else None

    def get_related_services(self):
        """Get other services in the same category at the same facility"""
        if not self.category or not self.facility_id:
            return []
        
        return Service.query.filter(
            Service.facility_id == self.facility_id,
            Service.category == self.category,
            Service.id != self.id
        ).all()

    def get_complementary_services(self):
        """Get services that complement this one (same skill type, different category)"""
        if not self.skill_type or not self.facility_id:
            return []
        
        return Service.query.filter(
            Service.facility_id == self.facility_id,
            Service.skill_type == self.skill_type,
            Service.category != self.category,
            Service.id != self.id
        ).all()

    def is_hardware_service(self):
        """Check if this is a hardware-related service"""
        return self.skill_type and 'hardware' in self.skill_type.lower()

    def is_software_service(self):
        """Check if this is a software-related service"""
        return self.skill_type and 'software' in self.skill_type.lower()

    def is_integration_service(self):
        """Check if this is an integration service"""
        return self.skill_type and 'integration' in self.skill_type.lower()

    def get_service_capabilities(self):
        """Get facility capabilities relevant to this service"""
        if not self.facility:
            return []
        
        facility_caps = self.facility.get_capabilities_list()
        service_keywords = []
        
        if self.category:
            service_keywords.append(self.category.lower())
        if self.skill_type:
            service_keywords.append(self.skill_type.lower())
        if self.name:
            service_keywords.extend(self.name.lower().split())
        
        # Filter facility capabilities that relate to this service
        relevant_caps = []
        for cap in facility_caps:
            cap_lower = cap.lower()
            if any(keyword in cap_lower for keyword in service_keywords):
                relevant_caps.append(cap)
        
        return relevant_caps

    def can_support_innovation_area(self, innovation_area):
        """Check if service can support a specific innovation area"""
        innovation_keywords = innovation_area.lower().split()
        service_text = f"{self.name} {self.description or ''} {self.category or ''} {self.skill_type or ''}".lower()
        
        return any(keyword in service_text for keyword in innovation_keywords)

    def get_usage_statistics(self):
        """Get statistics about how this service is being utilized"""
        # This would require additional tracking in a real application
        # For now, return basic info
        return {
            'facility_name': self.get_facility_name(),
            'facility_location': self.get_facility_location(),
            'category': self.category,
            'skill_type': self.skill_type,
            'related_services_count': len(self.get_related_services()),
            'complementary_services_count': len(self.get_complementary_services())
        }

    def get_service_portfolio(self):
        """Get the full service portfolio of the facility"""
        if not self.facility:
            return []
        
        return self.facility.services

    def to_dict(self, include_facility_info=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'facility_id': self.facility_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'skill_type': self.skill_type
        }
        
        if include_facility_info and self.facility:
            data.update({
                'facility_name': self.facility.name,
                'facility_location': self.facility.location,
                'facility_type': self.facility.facility_type,
                'partner_org': self.facility.partner_org,
                'related_services_count': len(self.get_related_services()),
                'relevant_capabilities': self.get_service_capabilities()
            })
        
        return data