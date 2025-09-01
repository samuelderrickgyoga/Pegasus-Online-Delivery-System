from flask import Blueprint, request, jsonify
from models.project import Project  # import the model directly

projects_bp = Blueprint('projects', __name__)

# Basic CRUD operations
@projects_bp.route('/', methods=['GET'])
def get_all_projects():
    """List all projects globally with optional filters"""
    filters = {
        'facility_id': request.args.get('facilityId'),
        'program_id': request.args.get('programId'),
        'prototype_stage': request.args.get('stage'),
        'innovation_focus': request.args.get('innovationFocus')
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    query = Project.query
    for key, value in filters.items():
        if key == 'innovation_focus':
            query = query.filter(Project.innovation_focus.ilike(f'%{value}%'))
        else:
            query = query.filter(getattr(Project, key) == value)
    
    projects = query.all()
    return jsonify([p.to_dict(include_relationships=True) for p in projects])

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    """View project details"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project.to_dict(include_relationships=True))

@projects_bp.route('/', methods=['POST'])
def create_project():
    """Create new project"""
    data = request.json
    project = Project.create(
        program_id=data.get('program_id'),
        facility_id=data.get('facility_id'),
        title=data.get('title'),
        nature=data.get('nature'),
        description=data.get('description'),
        innovation_focus=data.get('innovation_focus'),
        prototype_stage=data.get('prototype_stage'),
        testing_requirements=data.get('testing_requirements'),
        commercialization_plan=data.get('commercialization_plan')
    )
    return jsonify(project.to_dict(include_relationships=True)), 201

@projects_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Edit project details"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    project.update(**request.json)
    return jsonify(project.to_dict(include_relationships=True))

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete project"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    project.delete()
    return jsonify({'message': 'Project deleted successfully'})

# Participant management routes
@projects_bp.route('/<int:project_id>/participants', methods=['POST'])
def assign_participant(project_id):
    """Assign participant to project"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    data = request.json
    participant = data.get('participant')
    role = data.get('role')
    skill_role = data.get('skill_role')
    if not participant:
        return jsonify({'error': 'Participant data missing'}), 400
    # Assuming you have a ProjectParticipant relationship model
    project_participant = project.add_participant(participant, role, skill_role)
    return jsonify({'message': 'Participant assigned', 'participant': project_participant.to_dict()}), 201

@projects_bp.route('/<int:project_id>/participants/<int:participant_id>', methods=['DELETE'])
def remove_participant(project_id, participant_id):
    """Remove participant from project"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    success = project.remove_participant(participant_id)
    if not success:
        return jsonify({'error': 'Participant not found in project'}), 404
    return jsonify({'message': 'Participant removed successfully'})

@projects_bp.route('/<int:project_id>/participants', methods=['GET'])
def get_project_participants(project_id):
    """List project participants"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    participants = [pp.participant.to_dict() for pp in project.participants]
    return jsonify(participants)

# Related entity routes
@projects_bp.route('/<int:project_id>/outcomes', methods=['GET'])
def get_project_outcomes(project_id):
    """List outcomes for project"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    outcomes = [o.to_dict() for o in project.outcomes]
    return jsonify(outcomes)
