from flask import Blueprint, request, jsonify
from controllers.equipment_controller import EquipmentController

equipment_bp = Blueprint('equipment', __name__)
controller = EquipmentController()

# Basic CRUD operations
@equipment_bp.route('/', methods=['GET'])
def get_all_equipment():
    """List all equipment globally with optional filters"""
    # Handle filters: ?usageDomain=Electronics&supportPhase=Prototyping&facilityId=1
    filters = {
        'usage_domain': request.args.get('usageDomain'),
        'support_phase': request.args.get('supportPhase'),
        'facility_id': request.args.get('facilityId'),
        'capability': request.args.get('capability')
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_equipment(filters)

@equipment_bp.route('/search', methods=['GET'])
def search_equipment():
    """Search equipment by capability/usage domain"""
    search_params = request.args.to_dict()
    return controller.search_equipment(search_params)

@equipment_bp.route('/<int:equipment_id>', methods=['GET'])
def get_equipment_by_id(equipment_id):
    """View equipment details"""
    return controller.get_equipment_by_id(equipment_id)

@equipment_bp.route('/', methods=['POST'])
def create_equipment():
    """Create new equipment"""
    return controller.create_equipment(request.json)

@equipment_bp.route('/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """Edit equipment details"""
    return controller.update_equipment(equipment_id, request.json)

@equipment_bp.route('/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """Delete equipment"""
    return controller.delete_equipment(equipment_id)