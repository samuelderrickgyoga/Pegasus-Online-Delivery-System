from flask import Blueprint, request, jsonify
from controllers.project_controller import ProjectController

projects_bp = Blueprint('projects', __name__)
controller = ProjectController()

# Basic CRUD operations
@projects_bp.route('/', methods=['GET'])
def get_all_projects():
    """List all projects globally with optional filters"""
    # Handle filters: ?facilityId=1&programId=2&stage=Prototype
    filters = {
        'facility_id': request.args.get('facilityId'),
        'program_id': request.args.get('programId'),
        'prototype_stage': request.args.get('stage'),
        'innovation_focus': request.args.get('innovationFocus')
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_projects(filters)

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    """View project details"""
    return controller.get_project_by_id(project_id)

@projects_bp.route('/', methods=['POST'])
def create_project():
    """Create new project"""
    return controller.create_project(request.json)

@projects_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Edit project details"""
    return controller.update_project(project_id, request.json)

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete project"""
    return controller.delete_project(project_id)

# Participant management routes
@projects_bp.route('/<int:project_id>/participants', methods=['POST'])
def assign_participant(project_id):
    """Assign participant to project"""
    return controller.assign_participant(project_id, request.json)

@projects_bp.route('/<int:project_id>/participants/<int:participant_id>', methods=['DELETE'])
def remove_participant(project_id, participant_id):
    """Remove participant from project"""
    return controller.remove_participant(project_id, participant_id)

@projects_bp.route('/<int:project_id>/participants', methods=['GET'])
def get_project_participants(project_id):
    """List project participants"""
    return controller.get_project_participants(project_id)

# Related entity routes
@projects_bp.route('/<int:project_id>/outcomes', methods=['GET'])
def get_project_outcomes(project_id):
    """List outcomes for project"""
    return controller.get_project_outcomes(project_id)