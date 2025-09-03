from flask import jsonify
from app.models.participant import Participant
from app.models.project import Project
from app.models.project_participant import ProjectParticipant
from app.database import db

class ParticipantController:
    
    def get_all_participants(self, filters=None):
        """List all participants with optional filtering"""
        try:
            query = Participant.query
            
            if filters:
                if 'affiliation' in filters:
                    query = query.filter(Participant.affiliation == filters['affiliation'])
                if 'cross_skill_trained' in filters:
                    # Convert string to boolean
                    cross_skill_trained = filters['cross_skill_trained'].lower() == 'true'
                    query = query.filter(Participant.cross_skill_trained == cross_skill_trained)
                if 'institution' in filters:
                    query = query.filter(Participant.institution == filters['institution'])
                if 'specialization' in filters:
                    query = query.filter(Participant.specialization == filters['specialization'])
            
            participants = query.all()
            return jsonify([participant.to_dict() for participant in participants]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve participants: {str(e)}'}), 500
    
    def get_participant_by_id(self, participant_id):
        """Get participant details by ID"""
        try:
            participant = Participant.query.get(participant_id)
            if not participant:
                return jsonify({'error': 'Participant not found'}), 404
            return jsonify(participant.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve participant: {str(e)}'}), 500
    
    def create_participant(self, data):
        """Create new participant"""
        try:
            # Validate required fields
            required_fields = ['full_name', 'email', 'affiliation', 'institution']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Check if email already exists
            existing_participant = Participant.query.filter_by(email=data['email']).first()
            if existing_participant:
                return jsonify({'error': 'Email already registered'}), 400
            
            participant = Participant(
                full_name=data['full_name'],
                email=data['email'],
                affiliation=data['affiliation'],
                specialization=data.get('specialization'),
                cross_skill_trained=data.get('cross_skill_trained', False),
                institution=data['institution']
            )
            
            db.session.add(participant)
            db.session.commit()
            
            return jsonify(participant.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create participant: {str(e)}'}), 400
    
    def update_participant(self, participant_id, data):
        """Update participant details"""
        try:
            participant = Participant.query.get(participant_id)
            if not participant:
                return jsonify({'error': 'Participant not found'}), 404
            
            # Check email uniqueness if email is being updated
            if 'email' in data and data['email'] != participant.email:
                existing = Participant.query.filter_by(email=data['email']).first()
                if existing:
                    return jsonify({'error': 'Email already registered'}), 400
            
            updatable_fields = ['full_name', 'email', 'affiliation', 'specialization', 
                              'cross_skill_trained', 'institution']
            for field in updatable_fields:
                if field in data:
                    setattr(participant, field, data[field])
            
            db.session.commit()
            return jsonify(participant.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update participant: {str(e)}'}), 400
    
    def delete_participant(self, participant_id):
        """Delete participant (with dependency check)"""
        try:
            participant = Participant.query.get(participant_id)
            if not participant:
                return jsonify({'error': 'Participant not found'}), 404
            
            # Check for project associations
            project_count = ProjectParticipant.query.filter_by(participant_id=participant_id).count()
            if project_count > 0:
                return jsonify({
                    'error': f'Cannot delete participant. They are assigned to {project_count} projects.'
                }), 400
            
            db.session.delete(participant)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete participant: {str(e)}'}), 500
    
    def get_participant_projects(self, participant_id):
        """Get all projects for a participant"""
        try:
            participant = Participant.query.get(participant_id)
            if not participant:
                return jsonify({'error': 'Participant not found'}), 404
            
            # Query with join to get project details
            projects = db.session.query(
                Project, ProjectParticipant
            ).join(
                ProjectParticipant, Project.project_id == ProjectParticipant.project_id
            ).filter(
                ProjectParticipant.participant_id == participant_id
            ).all()
            
            result = []
            for project, project_participant in projects:
                project_data = project.to_dict()
                project_data.update({
                    'role_on_project': project_participant.role_on_project,
                    'skill_role': project_participant.skill_role
                })
                result.append(project_data)
            
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve projects: {str(e)}'}), 500
