from flask import jsonify
from app.models.equipment import Equipment
from app.models.facility import Facility
from app.database import db

class EquipmentController:
    
    def get_all_equipment(self, filters=None):
        """List all equipment with optional filtering"""
        try:
            query = Equipment.query
            
            if filters:
                if 'usage_domain' in filters:
                    query = query.filter(Equipment.usage_domain == filters['usage_domain'])
                if 'support_phase' in filters:
                    query = query.filter(Equipment.support_phase == filters['support_phase'])
                if 'facility_id' in filters:
                    query = query.filter(Equipment.facility_id == filters['facility_id'])
                if 'capability' in filters:
                    query = query.filter(Equipment.capabilities.ilike(f"%{filters['capability']}%"))
            
            equipment = query.all()
            return jsonify([eq.to_dict() for eq in equipment]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve equipment: {str(e)}'}), 500
    
    def search_equipment(self, search_params):
        """Search equipment by capability and usage domain"""
        try:
            query = Equipment.query
            
            for key, value in search_params.items():
                if key == 'name':
                    query = query.filter(Equipment.name.ilike(f"%{value}%"))
                elif key == 'capability':
                    query = query.filter(Equipment.capabilities.ilike(f"%{value}%"))
                elif key == 'usage_domain':
                    query = query.filter(Equipment.usage_domain == value)
                elif key == 'inventory_code':
                    query = query.filter(Equipment.inventory_code == value)
            
            equipment = query.all()
            return jsonify([eq.to_dict() for eq in equipment]), 200
        except Exception as e:
            return jsonify({'error': f'Search failed: {str(e)}'}), 500
    
    def get_equipment_by_id(self, equipment_id):
        """Get equipment details by ID"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                return jsonify({'error': 'Equipment not found'}), 404
            return jsonify(equipment.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve equipment: {str(e)}'}), 500
    
    def create_equipment(self, data):
        """Create new equipment"""
        try:
            # Validate required fields
            required_fields = ['facility_id', 'name', 'usage_domain']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Verify facility exists
            facility = Facility.query.get(data['facility_id'])
            if not facility:
                return jsonify({'error': 'Invalid facility_id'}), 400
            
            equipment = Equipment(
                facility_id=data['facility_id'],
                name=data['name'],
                capabilities=data.get('capabilities'),
                description=data.get('description'),
                inventory_code=data.get('inventory_code'),
                usage_domain=data['usage_domain'],
                support_phase=data.get('support_phase')
            )
            
            db.session.add(equipment)
            db.session.commit()
            
            return jsonify(equipment.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create equipment: {str(e)}'}), 400
    
    def update_equipment(self, equipment_id, data):
        """Update equipment details"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                return jsonify({'error': 'Equipment not found'}), 404
            
            # Validate facility_id if being updated
            if 'facility_id' in data:
                facility = Facility.query.get(data['facility_id'])
                if not facility:
                    return jsonify({'error': 'Invalid facility_id'}), 400
            
            updatable_fields = ['facility_id', 'name', 'capabilities', 'description', 
                              'inventory_code', 'usage_domain', 'support_phase']
            for field in updatable_fields:
                if field in data:
                    setattr(equipment, field, data[field])
            
            db.session.commit()
            return jsonify(equipment.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update equipment: {str(e)}'}), 400
    
    def delete_equipment(self, equipment_id):
        """Delete equipment"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                return jsonify({'error': 'Equipment not found'}), 404
            
            # Note: Add checks for active project usage if needed
            
            db.session.delete(equipment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete equipment: {str(e)}'}), 500
