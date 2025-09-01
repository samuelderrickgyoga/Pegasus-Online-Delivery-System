from flask import Blueprint, request, jsonify
from controllers.participant_controller import ParticipantController

participants_bp = Blueprint('participants', __name__)
controller = ParticipantController()

# Basic CRUD operations
@participants_bp.route('/', methods=['GET'])
def get_all_participants():
    """List all participants with optional filters"""
    # Handle filters: ?affiliation=CS&crossSkillTrained=true&institution=SCIT
    filters = {
        'affiliation': request.args.get('affiliation'),
        'cross_skill_trained': request.args.get('crossSkillTrained'),
        'institution': request.args.get('institution'),
        'specialization': request.args.get('specialization')
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_participants(filters)

@participants_bp.route('/<int:participant_id>', methods=['GET'])
def get_participant_by_id(participant_id):
    """View participant profile"""
    return controller.get_participant_by_id(participant_id)

@participants_bp.route('/', methods=['POST'])
def create_participant():
    """Create participant record"""
    return controller.create_participant(request.json)

@participants_bp.route('/<int:participant_id>', methods=['PUT'])
def update_participant(participant_id):
    """Edit participant details"""
    return controller.update_participant(participant_id, request.json)

@participants_bp.route('/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    """Delete participant"""
    return controller.delete_participant(participant_id)

# Related entity routes
@participants_bp.route('/<int:participant_id>/projects', methods=['GET'])
def get_participant_projects(participant_id):
    """List projects for participant"""
    return controller.get_participant_projects(participant_id)