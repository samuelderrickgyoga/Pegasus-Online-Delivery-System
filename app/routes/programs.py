from flask import Blueprint, request, jsonify
from app.controllers.program_controller import ProgramController

programs_bp = Blueprint('programs', __name__)
controller = ProgramController()

# Basic CRUD operations
@programs_bp.route('/', methods=['GET'])
def get_all_programs():
    """List all programs"""
    return controller.get_all_programs()

@programs_bp.route('/<int:program_id>', methods=['GET'])
def get_program_by_id(program_id):
    """View program details"""
    return controller.get_program_by_id(program_id)

@programs_bp.route('/', methods=['POST'])
def create_program():
    """Create new program"""
    return controller.create_program(request.json)

@programs_bp.route('/<int:program_id>', methods=['PUT'])
def update_program(program_id):
    """Edit program details"""
    return controller.update_program(program_id, request.json)

@programs_bp.route('/<int:program_id>', methods=['DELETE'])
def delete_program(program_id):
    """Delete program"""
    return controller.delete_program(program_id)

# Related entity routes
@programs_bp.route('/<int:program_id>/projects', methods=['GET'])
def get_projects_by_program(program_id):
    """List projects under program"""
    return controller.get_projects_by_program(program_id)