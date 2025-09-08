from flask import jsonify
from app.models.facility import Facility
from app.models.service import Service
from app.models.equipment import Equipment
from app.models.project import Project
from app import db

class FacilityController:
    
    def get_all_facilities(self, filters=None):
        """List all facilities with optional filtering"""
        try:
            query = Facility.query
            
            if filters:
                if 'type' in filters:
                    query = query.filter(Facility.facility_type == filters['type'])
                if 'partner' in filters:
                    query = query.filter(Facility.partner_organization.ilike(f"%{filters['partner']}%"))
                if 'location' in filters:
                    query = query.filter(Facility.location.ilike(f"%{filters['location']}%"))
                if 'capability' in filters:
                    query = query.filter(Facility.capabilities.ilike(f"%{filters['capability']}%"))
            
            facilities = query.all()
            return jsonify([facility.to_dict() for facility in facilities]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve facilities: {str(e)}'}), 500
    
    def search_facilities(self, search_params):
        """Advanced facility search"""
        try:
            query = Facility.query
            
            for key, value in search_params.items():
                if key == 'name':
                    query = query.filter(Facility.name.ilike(f"%{value}%"))
                elif key == 'description':
                    query = query.filter(Facility.description.ilike(f"%{value}%"))
                elif key == 'capability':
                    query = query.filter(Facility.capabilities.ilike(f"%{value}%"))
            
            facilities = query.all()
            return jsonify([facility.to_dict() for facility in facilities]), 200
        except Exception as e:
            return jsonify({'error': f'Search failed: {str(e)}'}), 500
    
    def get_facility_by_id(self, facility_id):
        """Get facility details by ID"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
            return jsonify(facility.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve facility: {str(e)}'}), 500
    
    def create_facility(self, data):
        """Create new facility"""
        try:
            # Validate required fields
            required_fields = ['name', 'location', 'facility_type']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            facility = Facility(
                name=data['name'],
                location=data['location'],
                description=data.get('description'),
                partner_organization=data.get('partner_organization'),
                facility_type=data['facility_type'],
                capabilities=data.get('capabilities')
            )
            
            db.session.add(facility)
            db.session.commit()
            
            return jsonify(facility.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create facility: {str(e)}'}), 400
    
    def update_facility(self, facility_id, data):
        """Update facility details"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
            
            updatable_fields = ['name', 'location', 'description', 'partner_organization', 
                              'facility_type', 'capabilities']
            for field in updatable_fields:
                if field in data:
                    setattr(facility, field, data[field])
            
            db.session.commit()
            return jsonify(facility.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update facility: {str(e)}'}), 400
    
    def delete_facility(self, facility_id):
        """Delete facility (with dependency checks)"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
            
            # Check dependencies
            service_count = Service.query.filter_by(facility_id=facility_id).count()
            equipment_count = Equipment.query.filter_by(facility_id=facility_id).count()
            project_count = Project.query.filter_by(facility_id=facility_id).count()
            
            dependencies = []
            if service_count > 0:
                dependencies.append(f'{service_count} services')
            if equipment_count > 0:
                dependencies.append(f'{equipment_count} equipment items')
            if project_count > 0:
                dependencies.append(f'{project_count} projects')
            
            if dependencies:
                return jsonify({
                    'error': f'Cannot delete facility. It has {", ".join(dependencies)} linked to it.'
                }), 400
            
            db.session.delete(facility)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete facility: {str(e)}'}), 500
    
    def get_services_by_facility(self, facility_id):
        """Get all services offered by a facility"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
                
            services = Service.query.filter_by(facility_id=facility_id).all()
            return jsonify([service.to_dict() for service in services]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve services: {str(e)}'}), 500
    
    def get_equipment_by_facility(self, facility_id):
        """Get all equipment at a facility"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
                
            equipment = Equipment.query.filter_by(facility_id=facility_id).all()
            return jsonify([eq.to_dict() for eq in equipment]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve equipment: {str(e)}'}), 500
    
    def get_projects_by_facility(self, facility_id):
        """Get all projects at a facility"""
        try:
            facility = Facility.query.get(facility_id)
            if not facility:
                return jsonify({'error': 'Facility not found'}), 404
                
            projects = Project.query.filter_by(facility_id=facility_id).all()
            return jsonify([project.to_dict() for project in projects]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve projects: {str(e)}'}), 500
