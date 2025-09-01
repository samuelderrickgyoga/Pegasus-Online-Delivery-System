from app import db



class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    capabilities = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    inventory_code = db.Column(db.String(100), nullable=True)
    usage_domain = db.Column(db.String(100), nullable=True)  # Electronics, Mechanical, IoT
    support_phase = db.Column(db.String(100), nullable=True)  # Training, Prototyping, etc.

    # Relationships
    facility = db.relationship("Facility", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment {self.name}>"
    
    
    @classmethod
    def create(cls, facility_id, name, capabilities=None, description=None, 
               inventory_code=None, usage_domain=None, support_phase=None):
        """Create new equipment"""
        equipment = cls(
            facility_id=facility_id,
            name=name,
            capabilities=capabilities,
            description=description,
            inventory_code=inventory_code,
            usage_domain=usage_domain,
            support_phase=support_phase
        )
        db.session.add(equipment)
        db.session.commit()
        return equipment

    @classmethod
    def get_by_id(cls, equipment_id):
        """Get equipment by ID"""
        return cls.query.get(equipment_id)

    @classmethod
    def get_by_name(cls, name):
        """Get equipment by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_inventory_code(cls, code):
        """Get equipment by inventory code"""
        return cls.query.filter_by(inventory_code=code).first()

    @classmethod
    def get_all(cls):
        """Get all equipment"""
        return cls.query.all()

    @classmethod
    def get_by_facility(cls, facility_id):
        """Get all equipment for a specific facility"""
        return cls.query.filter_by(facility_id=facility_id).all()

    @classmethod
    def get_by_domain(cls, usage_domain):
        """Get equipment by usage domain"""
        return cls.query.filter_by(usage_domain=usage_domain).all()

    @classmethod
    def get_by_phase(cls, support_phase):
        """Get equipment by support phase"""
        return cls.query.filter_by(support_phase=support_phase).all()

    @classmethod
    def search_by_capability(cls, capability):
        """Search equipment by capability"""
        return cls.query.filter(cls.capabilities.ilike(f'%{capability}%')).all()

    @classmethod
    def search_equipment(cls, query):
        """Search equipment by name, description, or capabilities"""
        return cls.query.filter(
            db.or_(
                cls.name.ilike(f'%{query}%'),
                cls.description.ilike(f'%{query}%'),
                cls.capabilities.ilike(f'%{query}%')
            )
        ).all()

    @classmethod
    def get_all_domains(cls):
        """Get all unique usage domains"""
        return [domain[0] for domain in cls.query.with_entities(cls.usage_domain).distinct().all() 
                if domain[0] is not None]

    @classmethod
    def get_all_phases(cls):
        """Get all unique support phases"""
        return [phase[0] for phase in cls.query.with_entities(cls.support_phase).distinct().all() 
                if phase[0] is not None]

    def update(self, **kwargs):
        """Update equipment attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete the equipment"""
        db.session.delete(self)
        db.session.commit()

    def get_capabilities_list(self):
        """Get capabilities as a list"""
        if self.capabilities:
            return [cap.strip() for cap in self.capabilities.split(',')]
        return []

    def add_capability(self, capability):
        """Add a new capability to the equipment"""
        current_caps = self.get_capabilities_list()
        if capability not in current_caps:
            current_caps.append(capability)
            self.capabilities = ', '.join(current_caps)
            db.session.commit()

    def remove_capability(self, capability):
        """Remove a capability from the equipment"""
        current_caps = self.get_capabilities_list()
        if capability in current_caps:
            current_caps.remove(capability)
            self.capabilities = ', '.join(current_caps) if current_caps else None
            db.session.commit()

    def has_capability(self, capability):
        """Check if equipment has a specific capability"""
        return capability.lower() in [cap.lower() for cap in self.get_capabilities_list()]

    def get_facility_name(self):
        """Get the name of the facility housing this equipment"""
        return self.facility.name if self.facility else None

    def get_facility_location(self):
        """Get the location of the facility housing this equipment"""
        return self.facility.location if self.facility else None

    def get_similar_equipment(self):
        """Get equipment with similar capabilities at the same facility"""
        if not self.facility_id:
            return []
        
        equipment_list = []
        current_caps = [cap.lower() for cap in self.get_capabilities_list()]
        
        for equipment in self.facility.equipment:
            if equipment.id == self.id:
                continue
                
            equipment_caps = [cap.lower() for cap in equipment.get_capabilities_list()]
            # Check if there's any overlap in capabilities
            if any(cap in equipment_caps for cap in current_caps):
                equipment_list.append(equipment)
        
        return equipment_list

    def get_domain_related_equipment(self):
        """Get equipment in the same usage domain at the facility"""
        if not self.usage_domain or not self.facility_id:
            return []
        
        return Equipment.query.filter(
            Equipment.facility_id == self.facility_id,
            Equipment.usage_domain == self.usage_domain,
            Equipment.id != self.id
        ).all()

    def get_phase_related_equipment(self):
        """Get equipment that supports the same phase"""
        if not self.support_phase or not self.facility_id:
            return []
        
        return Equipment.query.filter(
            Equipment.facility_id == self.facility_id,
            Equipment.support_phase == self.support_phase,
            Equipment.id != self.id
        ).all()

    def can_support_innovation_area(self, innovation_area):
        """Check if equipment can support a specific innovation area"""
        innovation_keywords = innovation_area.lower().split()
        equipment_text = f"{self.name} {self.description or ''} {self.capabilities or ''} {self.usage_domain or ''}".lower()
        
        return any(keyword in equipment_text for keyword in innovation_keywords)

    def is_suitable_for_phase(self, phase):
        """Check if equipment is suitable for a specific project phase"""
        if not self.support_phase:
            return True  # If no specific phase restriction, assume suitable for all
        
        return phase.lower() in self.support_phase.lower()

    def is_electronics_equipment(self):
        """Check if this is electronics equipment"""
        return self.usage_domain and 'electronics' in self.usage_domain.lower()

    def is_mechanical_equipment(self):
        """Check if this is mechanical equipment"""
        return self.usage_domain and 'mechanical' in self.usage_domain.lower()

    def is_iot_equipment(self):
        """Check if this is IoT equipment"""
        return self.usage_domain and 'iot' in self.usage_domain.lower()

    def supports_training(self):
        """Check if equipment supports training phase"""
        return self.support_phase and 'training' in self.support_phase.lower()

    def supports_prototyping(self):
        """Check if equipment supports prototyping phase"""
        return self.support_phase and 'prototyping' in self.support_phase.lower()

    def get_equipment_utilization_potential(self):
        """Get potential utilization based on equipment capabilities and facility projects"""
        if not self.facility:
            return {}
        
        potential_projects = []
        for project in self.facility.projects:
            if self.can_support_project(project):
                potential_projects.append(project)
        
        return {
            'suitable_projects': len(potential_projects),
            'total_facility_projects': len(self.facility.projects),
            'utilization_potential': round(
                (len(potential_projects) / max(1, len(self.facility.projects))) * 100, 2
            ),
            'domain_match': self.usage_domain,
            'phase_support': self.support_phase
        }

    def can_support_project(self, project):
        """Check if this equipment can support a specific project"""
        if not project:
            return False
        
        # Check domain compatibility
        if project.innovation_focus and self.usage_domain:
            innovation_keywords = project.innovation_focus.lower().split()
            domain_keywords = self.usage_domain.lower().split()
            domain_match = any(keyword in project.innovation_focus.lower() 
                             for keyword in domain_keywords)
        else:
            domain_match = True
        
        # Check phase compatibility
        if project.prototype_stage and self.support_phase:
            phase_match = self.is_suitable_for_phase(project.prototype_stage)
        else:
            phase_match = True
        
        return domain_match and phase_match

    def get_maintenance_info(self):
        """Get equipment maintenance and status information"""
        return {
            'inventory_code': self.inventory_code,
            'facility': self.get_facility_name(),
            'location': self.get_facility_location(),
            'domain': self.usage_domain,
            'support_phases': self.support_phase,
            'capabilities_count': len(self.get_capabilities_list()),
            'similar_equipment_count': len(self.get_similar_equipment())
        }

    def get_capability_matrix(self):
        """Get a matrix of capabilities and their applications"""
        capabilities = self.get_capabilities_list()
        matrix = {}
        
        for capability in capabilities:
            matrix[capability] = {
                'domain': self.usage_domain,
                'phase': self.support_phase,
                'facility': self.get_facility_name(),
                'related_equipment': [eq.name for eq in self.get_similar_equipment()]
            }
        
        return matrix

    def to_dict(self, include_facility_info=False, include_related=False):
        """Convert to dictionary representation"""
        data = {
            'id': self.id,
            'facility_id': self.facility_id,
            'name': self.name,
            'capabilities': self.get_capabilities_list(),
            'description': self.description,
            'inventory_code': self.inventory_code,
            'usage_domain': self.usage_domain,
            'support_phase': self.support_phase
        }
        
        if include_facility_info and self.facility:
            data.update({
                'facility_name': self.facility.name,
                'facility_location': self.facility.location,
                'facility_type': self.facility.facility_type,
                'partner_org': self.facility.partner_org
            })
        
        if include_related:
            data.update({
                'similar_equipment': [eq.to_dict() for eq in self.get_similar_equipment()],
                'domain_related_equipment': [eq.to_dict() for eq in self.get_domain_related_equipment()],
                'utilization_potential': self.get_equipment_utilization_potential(),
                'maintenance_info': self.get_maintenance_info()
            })
        
        return data    