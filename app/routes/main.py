from flask import Flask, render_template, Blueprint, session, redirect, url_for

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
