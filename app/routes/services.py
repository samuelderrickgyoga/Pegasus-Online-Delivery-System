from flask import Blueprint, request, jsonify
from models.service import Service  # import model directly

services_bp = Blueprint('services', __name__)

# Basic CRUD operations
@services_bp.route('/', methods=['GET'])
def get_all_services():
    """List all services with optional filters"""
    filters = {
        'category': request.args.get('category'),
        'skill_type': request.args.get('skillType'),
        'facility_id': request.args.get('facilityId')
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    query = Service.query
    for key, value in filters.items():
        query = query.filter(getattr(Service, key) == value)
    
    services = query.all()
    return jsonify([s.to_dict(include_facility_info=True) for s in services])

@services_bp.route('/search', methods=['GET'])
def search_services():
    """Search services by name or description"""
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    services = Service.search_services(query)
    return jsonify([s.to_dict(include_facility_info=True) for s in services])

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    """View service details"""
    service = Service.get_by_id(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service.to_dict(include_facility_info=True))

@services_bp.route('/', methods=['POST'])
def create_service():
    """Create new service"""
    data = request.json
    service = Service.create(
        facility_id=data.get('facility_id'),
        name=data.get('name'),
        description=data.get('description'),
        category=data.get('category'),
        skill_type=data.get('skill_type')
    )
    return jsonify(service.to_dict(include_facility_info=True)), 201

@services_bp.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    """Edit service details"""
    service = Service.get_by_id(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    service.update(**request.json)
    return jsonify(service.to_dict(include_facility_info=True))

@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Delete service"""
    service = Service.get_by_id(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    service.delete()
    return jsonify({'message': 'Service deleted successfully'})
