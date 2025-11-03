from flask import Flask, render_template, Blueprint, session, redirect, url_for, send_from_directory, abort
import os
import glob

from app.models.program import Program
from app.models.facility import Facility
from app.models.equipment import Equipment
from app.models.project import Project
from app.models.participant import Participant
from app.models.outcome import Outcome
from app.models.service import Service

# from app.models.facility import Product 
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/projects')
def projects():
    return render_template('projects.html')

@main_bp.route('/equipment')
def equipment():
    return render_template('equipment.html')

@main_bp.route('/facilities')
def facilities():
    return render_template('facilities.html')

@main_bp.route('/participants')
def participants():
    return render_template('participants.html')

@main_bp.route('/participants/<int:user_id>')
def participant_detail(user_id):
    return render_template('participants.html', user_id=user_id)

@main_bp.route('/participants/<int:user_id>', methods=['PUT'])
def update_participants(user_id):
    # TO BE IMPLEMENTED 
    return render_template('participants.html', user_id=user_id)

@main_bp.route('/outcomes')
def outcomes():
    return render_template('outcomes.html')

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/programs')
def programs():
    return render_template('programs.html', products=[], user_role=None)


@main_bp.route('/analytics')
def analytics():
    """Analytics page: interactive charts + gallery of generated PNG visuals."""
    # Compute entity counts
    entity_counts = {
        'Programs': Program.query.count(),
        'Facilities': Facility.query.count(),
        'Equipment': Equipment.query.count(),
        'Projects': Project.query.count(),
        'Participants': Participant.query.count(),
        'Outcomes': Outcome.query.count(),
        'Services': Service.query.count(),
    }

    # Outcome commercialization distribution (if any)
    try:
        statuses = {}
        for o in Outcome.query.all():
            key = (o.commercialization_status or 'Unknown')
            statuses[key] = statuses.get(key, 0) + 1
    except Exception:
        statuses = {}

    # Find generated visualization images in repo root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    pattern = os.path.join(base_dir, 'visualization_*.png')
    image_paths = sorted(glob.glob(pattern))
    image_files = [os.path.basename(p) for p in image_paths]

    return render_template(
        'analytics.html',
        entity_labels=list(entity_counts.keys()),
        entity_values=list(entity_counts.values()),
        status_labels=list(statuses.keys()),
        status_values=list(statuses.values()),
        image_files=image_files
    )


@main_bp.route('/analytics/images/<path:filename>')
def analytics_image(filename: str):
    """Serve generated visualization images safely from repo root."""
    # Security: only allow visualization_*.png from the project root
    if not (filename.startswith('visualization_') and filename.endswith('.png') and '/' not in filename and '\\' not in filename):
        abort(404)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return send_from_directory(base_dir, filename)
