from flask import jsonify
from app.models.service import Service
from app.models.facility import Facility
from app import db

class ServiceController:
    
    def get_all_services(self, filters=None):
        """List all services with optional filtering"""
        try:
            query = Service.query
            
            if filters:
                if 'category' in filters:
                    query = query.filter(Service.category == filters['category'])
                if 'skill_type' in filters:
                    query = query.filter(Service.skill_type == filters['skill_type'])
                if 'facility_id' in filters:
                    query = query.filter(Service.facility_id == filters['facility_id'])
            
            services = query.all()
            return jsonify([service.to_dict() for service in services]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve services: {str(e)}'}), 500
    
    def search_services(self, search_params):
        """Search services by various criteria"""
        try:
            query = Service.query
            
            for key, value in search_params.items():
                if key == 'name':
                    query = query.filter(Service.name.ilike(f"%{value}%"))
                elif key == 'description':
                    query = query.filter(Service.description.ilike(f"%{value}%"))
                elif key == 'category':
                    query = query.filter(Service.category == value)
            
            services = query.all()
            return jsonify([service.to_dict() for service in services]), 200
        except Exception as e:
            return jsonify({'error': f'Search failed: {str(e)}'}), 500
    
    def get_service_by_id(self, service_id):
        """Get service details by ID"""
        try:
            service = Service.query.get(service_id)
            if not service:
                return jsonify({'error': 'Service not found'}), 404
            return jsonify(service.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve service: {str(e)}'}), 500
    
    def create_service(self, data):
        """Create new service"""
        try:
            # Validate required fields
            required_fields = ['facility_id', 'name', 'category']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Verify facility exists
            facility = Facility.query.get(data['facility_id'])
            if not facility:
                return jsonify({'error': 'Invalid facility_id'}), 400
            
            service = Service(
                facility_id=data['facility_id'],
                name=data['name'],
                description=data.get('description'),
                category=data['category'],
                skill_type=data.get('skill_type')
            )
            
            db.session.add(service)
            db.session.commit()
            
            return jsonify(service.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create service: {str(e)}'}), 400
    
    def update_service(self, service_id, data):
        """Update service details"""
        try:
            service = Service.query.get(service_id)
            if not service:
                return jsonify({'error': 'Service not found'}), 404
            
            # Validate facility_id if being updated
            if 'facility_id' in data:
                facility = Facility.query.get(data['facility_id'])
                if not facility:
                    return jsonify({'error': 'Invalid facility_id'}), 400
            
            updatable_fields = ['facility_id', 'name', 'description', 'category', 'skill_type']
            for field in updatable_fields:
                if field in data:
                    setattr(service, field, data[field])
            
            db.session.commit()
            return jsonify(service.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update service: {str(e)}'}), 400
    
    def delete_service(self, service_id):
        """Delete service"""
        try:
            service = Service.query.get(service_id)
            if not service:
                return jsonify({'error': 'Service not found'}), 404
            
            db.session.delete(service)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete service: {str(e)}'}), 500
