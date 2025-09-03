from flask import Blueprint, request, jsonify
from app.controllers.facility_controller import FacilityController

facilities_bp = Blueprint('facilities', __name__)
controller = FacilityController()

# Basic CRUD operations
@facilities_bp.route('/', methods=['GET'])
def get_all_facilities():
    """List all facilities with optional search/filter"""
    # Handle search parameters: ?type=Lab&partner=UIRI&capability=CNC
    filters = {
        'type': request.args.get('type'),
        'partner': request.args.get('partner'),
        'capability': request.args.get('capability'),
        'location': request.args.get('location')
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_facilities(filters)

@facilities_bp.route('/search', methods=['GET'])
def search_facilities():
    """Advanced search facilities"""
    search_params = request.args.to_dict()
    return controller.search_facilities(search_params)

@facilities_bp.route('/<int:facility_id>', methods=['GET'])
def get_facility_by_id(facility_id):
    """View facility details"""
    return controller.get_facility_by_id(facility_id)

@facilities_bp.route('/', methods=['POST'])
def create_facility():
    """Create new facility"""
    return controller.create_facility(request.json)

@facilities_bp.route('/<int:facility_id>', methods=['PUT'])
def update_facility(facility_id):
    """Edit facility details"""
    return controller.update_facility(facility_id, request.json)

@facilities_bp.route('/<int:facility_id>', methods=['DELETE'])
def delete_facility(facility_id):
    """Delete facility"""
    return controller.delete_facility(facility_id)

# Related entity routes
@facilities_bp.route('/<int:facility_id>/services', methods=['GET'])
def get_services_by_facility(facility_id):
    """List services offered by facility"""
    return controller.get_services_by_facility(facility_id)

@facilities_bp.route('/<int:facility_id>/equipment', methods=['GET'])
def get_equipment_by_facility(facility_id):
    """List equipment at facility"""
    return controller.get_equipment_by_facility(facility_id)

@facilities_bp.route('/<int:facility_id>/projects', methods=['GET'])
def get_projects_by_facility(facility_id):
    """List projects at facility"""
    return controller.get_projects_by_facility(facility_id)