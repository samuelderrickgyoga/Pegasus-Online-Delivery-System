from flask import Blueprint, request, jsonify
from app.controllers.service_controller import ServiceController

services_bp = Blueprint('services', __name__)
controller = ServiceController()

# Basic CRUD operations
@services_bp.route('/', methods=['GET'])
def get_all_services():
    """List all services globally with optional filters"""
    # Handle filters: ?category=Machining&skillType=Hardware&facilityId=1
    filters = {
        'category': request.args.get('category'),
        'skill_type': request.args.get('skillType'),
        'facility_id': request.args.get('facilityId')
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_services(filters)

@services_bp.route('/search', methods=['GET'])
def search_services():
    """Search services by category"""
    search_params = request.args.to_dict()
    return controller.search_services(search_params)

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    """View service details"""
    return controller.get_service_by_id(service_id)

@services_bp.route('/', methods=['POST'])
def create_service():
    """Create new service"""
    return controller.create_service(request.json)

@services_bp.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    """Edit service details"""
    return controller.update_service(service_id, request.json)

@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Delete service"""
    return controller.delete_service(service_id)