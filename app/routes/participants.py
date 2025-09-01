from flask import Blueprint, request, jsonify
from models.participant import Participant  # import the model directly

participants_bp = Blueprint('participants', __name__)

# Basic CRUD operations
@participants_bp.route('/', methods=['GET'])
def get_all_participants():
    """List all participants with optional filters"""
    filters = {
        'affiliation': request.args.get('affiliation'),
        'cross_skill_trained': request.args.get('crossSkillTrained'),
        'institution': request.args.get('institution'),
        'specialization': request.args.get('specialization')
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    query = Participant.query
    for key, value in filters.items():
        if key == 'cross_skill_trained':
            value = value.lower() == 'true'
        query = query.filter(getattr(Participant, key) == value)
    
    participants = query.all()
    return jsonify([p.to_dict() for p in participants])

@participants_bp.route('/<int:participant_id>', methods=['GET'])
def get_participant_by_id(participant_id):
    """View participant profile"""
    participant = Participant.get_by_id(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    return jsonify(participant.to_dict(include_metrics=True, include_projects=True))

@participants_bp.route('/', methods=['POST'])
def create_participant():
    """Create participant record"""
    data = request.json
    participant = Participant.create(
        full_name=data.get('full_name'),
        email=data.get('email'),
        affiliation=data.get('affiliation'),
        specialization=data.get('specialization'),
        cross_skill_trained=data.get('cross_skill_trained', False),
        institution=data.get('institution')
    )
    return jsonify(participant.to_dict()), 201

@participants_bp.route('/<int:participant_id>', methods=['PUT'])
def update_participant(participant_id):
    """Edit participant details"""
    participant = Participant.get_by_id(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    participant.update(**request.json)
    return jsonify(participant.to_dict())

@participants_bp.route('/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    """Delete participant"""
    participant = Participant.get_by_id(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    try:
        participant.delete()
        return jsonify({'message': 'Participant deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Related entity routes
@participants_bp.route('/<int:participant_id>/projects', methods=['GET'])
def get_participant_projects(participant_id):
    """List projects for participant"""
    participant = Participant.get_by_id(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    projects = [p.to_dict() for p in participant.get_projects_list()]
    return jsonify(projects)
