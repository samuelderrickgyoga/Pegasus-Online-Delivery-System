from flask import jsonify
from app.models.outcome import Outcome
from app.models.project import Project
from app.database import db
import os

class OutcomeController:
    
    def get_all_outcomes(self, filters=None):
        """List all outcomes with optional filtering (admin use)"""
        try:
            query = Outcome.query
            
            if filters:
                if 'project_id' in filters:
                    query = query.filter(Outcome.project_id == filters['project_id'])
                if 'outcome_type' in filters:
                    query = query.filter(Outcome.outcome_type == filters['outcome_type'])
                if 'commercialization_status' in filters:
                    query = query.filter(Outcome.commercialization_status == filters['commercialization_status'])
            
            outcomes = query.all()
            return jsonify([outcome.to_dict() for outcome in outcomes]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve outcomes: {str(e)}'}), 500
    
    def get_outcome_by_id(self, outcome_id):
        """Get outcome details by ID"""
        try:
            outcome = Outcome.query.get(outcome_id)
            if not outcome:
                return jsonify({'error': 'Outcome not found'}), 404
            return jsonify(outcome.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve outcome: {str(e)}'}), 500
    
    def create_outcome(self, data):
        """Create new outcome with optional file upload"""
        try:
            # Validate required fields
            required_fields = ['project_id', 'title', 'outcome_type']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Verify project exists
            project = Project.query.get(data['project_id'])
            if not project:
                return jsonify({'error': 'Invalid project_id'}), 400
            
            # Handle artifact link (either uploaded file path or external URL)
            artifact_link = data.get('artifact_file') or data.get('artifact_link')
            
            outcome = Outcome(
                project_id=data['project_id'],
                title=data['title'],
                description=data.get('description'),
                artifact_link=artifact_link,
                outcome_type=data['outcome_type'],
                quality_certification=data.get('quality_certification'),
                commercialization_status=data.get('commercialization_status', 'In Development')
            )
            
            db.session.add(outcome)
            db.session.commit()
            
            return jsonify(outcome.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create outcome: {str(e)}'}), 400
    
    def update_outcome(self, outcome_id, data):
        """Update outcome details"""
        try:
            outcome = Outcome.query.get(outcome_id)
            if not outcome:
                return jsonify({'error': 'Outcome not found'}), 404
            
            # Validate project_id if being updated
            if 'project_id' in data:
                project = Project.query.get(data['project_id'])
                if not project:
                    return jsonify({'error': 'Invalid project_id'}), 400
            
            # Handle new artifact upload
            if data.get('artifact_file'):
                # Remove old file if it exists and is a local file
                if outcome.artifact_link and outcome.artifact_link.startswith('uploads/'):
                    try:
                        os.remove(outcome.artifact_link)
                    except OSError:
                        pass  # File may not exist or be deletable
                
                data['artifact_link'] = data.pop('artifact_file')
            
            updatable_fields = ['project_id', 'title', 'description', 'artifact_link',
                              'outcome_type', 'quality_certification', 'commercialization_status']
            for field in updatable_fields:
                if field in data:
                    setattr(outcome, field, data[field])
            
            db.session.commit()
            return jsonify(outcome.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update outcome: {str(e)}'}), 400
    
    def delete_outcome(self, outcome_id):
        """Delete outcome and associated file"""
        try:
            outcome = Outcome.query.get(outcome_id)
            if not outcome:
                return jsonify({'error': 'Outcome not found'}), 404
            
            # Remove associated file if it's a local upload
            if outcome.artifact_link and outcome.artifact_link.startswith('uploads/'):
                try:
                    os.remove(outcome.artifact_link)
                except OSError:
                    pass  # File may not exist
            
            db.session.delete(outcome)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete outcome: {str(e)}'}), 500
    
    def get_artifact_path(self, outcome_id):
        """Get file path for artifact download/view"""
        try:
            outcome = Outcome.query.get(outcome_id)
            if not outcome:
                return None
            
            # Return path only if it's a local file
            if outcome.artifact_link and outcome.artifact_link.startswith('uploads/'):
                return outcome.artifact_link
            return None
        except Exception as e:
            return None