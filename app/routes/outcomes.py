from flask import Blueprint, request, jsonify, send_file
from models.outcome import Outcome
from werkzeug.utils import secure_filename
import os

outcomes_bp = Blueprint("outcomes", __name__, url_prefix="/api/outcomes")

# Configure upload settings
UPLOAD_FOLDER = "uploads/outcomes"
ALLOWED_EXTENSIONS = {
    "txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "zip", "dwg", "step", "stl"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Basic CRUD
@outcomes_bp.route("/", methods=["GET"])
def get_all_outcomes():
    """List all outcomes with optional filters"""
    project_id = request.args.get("projectId", type=int)
    outcome_type = request.args.get("type")
    commercialization_status = request.args.get("commercializationStatus")

    if project_id:
        outcomes = Outcome.get_by_project(project_id)
    elif outcome_type:
        outcomes = Outcome.get_by_type(outcome_type)
    elif commercialization_status:
        outcomes = Outcome.get_by_commercialization_status(commercialization_status)
    else:
        outcomes = Outcome.get_all()

    return jsonify([o.to_dict(include_project_info=True, include_metrics=True) for o in outcomes]), 200


@outcomes_bp.route("/<int:outcome_id>", methods=["GET"])
def get_outcome_by_id(outcome_id):
    """View outcome details"""
    outcome = Outcome.get_by_id(outcome_id)
    if not outcome:
        return jsonify({"error": "Outcome not found"}), 404
    return jsonify(outcome.to_dict(include_project_info=True, include_metrics=True)), 200


@outcomes_bp.route("/", methods=["POST"])
def create_outcome():
    """Upload and create a new outcome"""
    artifact_file = None
    if "artifact" in request.files:
        file = request.files["artifact"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            artifact_file = file_path

    data = request.form.to_dict() or request.get_json()
    try:
        outcome = Outcome.create(
            project_id=data["project_id"],
            title=data["title"],
            description=data.get("description"),
            artifact_link=artifact_file or data.get("artifact_link"),
            outcome_type=data.get("outcome_type"),
            quality_certification=data.get("quality_certification"),
            commercialization_status=data.get("commercialization_status"),
        )
        return jsonify(outcome.to_dict(include_project_info=True)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@outcomes_bp.route("/<int:outcome_id>", methods=["PUT"])
def update_outcome(outcome_id):
    """Update outcome details"""
    outcome = Outcome.get_by_id(outcome_id)
    if not outcome:
        return jsonify({"error": "Outcome not found"}), 404

    artifact_file = None
    if "artifact" in request.files:
        file = request.files["artifact"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            artifact_file = file_path

    data = request.form.to_dict() or request.get_json()
    if artifact_file:
        data["artifact_link"] = artifact_file

    try:
        updated = outcome.update(**data)
        return jsonify(updated.to_dict(include_project_info=True, include_metrics=True)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@outcomes_bp.route("/<int:outcome_id>", methods=["DELETE"])
def delete_outcome(outcome_id):
    """Delete outcome"""
    outcome = Outcome.get_by_id(outcome_id)
    if not outcome:
        return jsonify({"error": "Outcome not found"}), 404
    try:
        outcome.delete()
        return jsonify({"message": "Outcome deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ------------------------------
# File operations
# ------------------------------

@outcomes_bp.route("/<int:outcome_id>/download", methods=["GET"])
def download_artifact(outcome_id):
    """Download artifact file"""
    outcome = Outcome.get_by_id(outcome_id)
    if not outcome or not outcome.artifact_link or not os.path.exists(outcome.artifact_link):
        return jsonify({"error": "File not found"}), 404
    return send_file(outcome.artifact_link, as_attachment=True)


@outcomes_bp.route("/<int:outcome_id>/view", methods=["GET"])
def view_artifact(outcome_id):
    """View artifact (for images/PDFs)"""
    outcome = Outcome.get_by_id(outcome_id)
    if not outcome or not outcome.artifact_link or not os.path.exists(outcome.artifact_link):
        return jsonify({"error": "File not found"}), 404
    return send_file(outcome.artifact_link)
