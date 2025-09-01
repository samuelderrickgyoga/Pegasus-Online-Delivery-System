from flask import Blueprint, request, jsonify
from models.program import Program

programs_bp = Blueprint("programs", __name__, url_prefix="/api/programs")

# Basic CRUD operations
@programs_bp.route("/", methods=["GET"])
def get_all_programs():
    """List all programs"""
    programs = Program.get_all()
    return jsonify([p.to_dict() for p in programs]), 200


@programs_bp.route("/<int:program_id>", methods=["GET"])
def get_program_by_id(program_id):
    """View program details"""
    program = Program.get_by_id(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify(program.to_dict(include_projects=True)), 200


@programs_bp.route("/", methods=["POST"])
def create_program():
    """Create new program"""
    data = request.get_json()
    try:
        program = Program.create(
            name=data.get("name"),
            description=data.get("description"),
            national_alignment=data.get("national_alignment"),
            focus_areas=data.get("focus_areas"),
            phases=data.get("phases"),
        )
        return jsonify(program.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@programs_bp.route("/<int:program_id>", methods=["PUT"])
def update_program(program_id):
    """Edit program details"""
    program = Program.get_by_id(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    try:
        updated = program.update(**request.get_json())
        return jsonify(updated.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@programs_bp.route("/<int:program_id>", methods=["DELETE"])
def delete_program(program_id):
    """Delete program"""
    program = Program.get_by_id(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    try:
        program.delete()
        return jsonify({"message": "Program deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@programs_bp.route("/<int:program_id>/projects", methods=["GET"])
def get_projects_by_program(program_id):
    """List projects under program"""
    program = Program.get_by_id(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify([p.to_dict() for p in program.projects]), 200
