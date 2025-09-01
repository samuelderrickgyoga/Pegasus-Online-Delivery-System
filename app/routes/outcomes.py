from flask import Blueprint, request, jsonify, send_file
from controllers.outcome_controller import OutcomeController
from werkzeug.utils import secure_filename
import os

outcomes_bp = Blueprint('outcomes', __name__)
controller = OutcomeController()

# Configure upload settings
UPLOAD_FOLDER = 'uploads/outcomes'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'dwg', 'step', 'stl'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Basic CRUD operations
@outcomes_bp.route('/', methods=['GET'])
def get_all_outcomes():
    """List all outcomes (admin use) with optional filters"""
    filters = {
        'project_id': request.args.get('projectId'),
        'outcome_type': request.args.get('type'),
        'commercialization_status': request.args.get('commercializationStatus')
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return controller.get_all_outcomes(filters)

@outcomes_bp.route('/<int:outcome_id>', methods=['GET'])
def get_outcome_by_id(outcome_id):
    """View outcome details"""
    return controller.get_outcome_by_id(outcome_id)

@outcomes_bp.route('/', methods=['POST'])
def create_outcome():
    """Upload new outcome"""
    # Handle file upload
    artifact_file = None
    if 'artifact' in request.files:
        file = request.files['artifact']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            artifact_file = file_path
    
    # Get form data
    outcome_data = request.form.to_dict()
    outcome_data['artifact_file'] = artifact_file
    
    return controller.create_outcome(outcome_data)

@outcomes_bp.route('/<int:outcome_id>', methods=['PUT'])
def update_outcome(outcome_id):
    """Edit outcome details"""
    # Handle optional file upload
    artifact_file = None
    if 'artifact' in request.files:
        file = request.files['artifact']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            artifact_file = file_path
    
    outcome_data = request.form.to_dict()
    outcome_data['artifact_file'] = artifact_file
    
    return controller.update_outcome(outcome_id, outcome_data)

@outcomes_bp.route('/<int:outcome_id>', methods=['DELETE'])
def delete_outcome(outcome_id):
    """Delete outcome"""
    return controller.delete_outcome(outcome_id)

# File operations
@outcomes_bp.route('/<int:outcome_id>/download', methods=['GET'])
def download_artifact(outcome_id):
    """Download artifact file"""
    file_path = controller.get_artifact_path(outcome_id)
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@outcomes_bp.route('/<int:outcome_id>/view', methods=['GET'])
def view_artifact(outcome_id):
    """View artifact (for images/PDFs)"""
    file_path = controller.get_artifact_path(outcome_id)
    if file_path and os.path.exists(file_path):
        return send_file(file_path)
    return jsonify({'error': 'File not found'}), 404