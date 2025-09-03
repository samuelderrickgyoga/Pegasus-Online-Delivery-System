from flask import jsonify
from app.models.project import Project
from app.models.program import Program
from app.models.facility import Facility
from app.models.participant import Participant
from app.models.project_participant import ProjectParticipant
from app.models.outcome import Outcome
from app.database import db

class ProjectController:
    
    def get_all_projects(self, filters=None):
        """List all projects with optional filtering"""
        try:
            query = Project.query
            
            if filters:
                if 'facility_id' in filters:
                    query = query.filter(Project.facility_id == filters['facility_id'])
                if 'program_id' in filters:
                    query = query.filter(Project.program_id == filters['program_id'])
                if 'prototype_stage' in filters:
                    query = query.filter(Project.prototype_stage == filters['prototype_stage'])
                if 'innovation_focus' in filters:
                    query = query.filter(Project.innovation_focus.ilike(f"%{filters['innovation_focus']}%"))
            
            projects = query.all()
            return jsonify([project.to_dict() for project in projects]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve projects: {str(e)}'}), 500
    
    def get_project_by_id(self, project_id):
        """Get project details by ID"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            return jsonify(project.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve project: {str(e)}'}), 500
    
    def create_project(self, data):
        """Create new project"""
        try:
            # Validate required fields
            required_fields = ['program_id', 'facility_id', 'title', 'nature_of_project']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Verify program and facility exist
            program = Program.query.get(data['program_id'])
            if not program:
                return jsonify({'error': 'Invalid program_id'}), 400
                
            facility = Facility.query.get(data['facility_id'])
            if not facility:
                return jsonify({'error': 'Invalid facility_id'}), 400
            
            project = Project(
                program_id=data['program_id'],
                facility_id=data['facility_id'],
                title=data['title'],
                nature_of_project=data['nature_of_project'],
                description=data.get('description'),
                innovation_focus=data.get('innovation_focus'),
                prototype_stage=data.get('prototype_stage'),
                testing_requirements=data.get('testing_requirements'),
                commercialization_plan=data.get('commercialization_plan')
            )
            
            db.session.add(project)
            db.session.commit()
            
            return jsonify(project.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create project: {str(e)}'}), 400
    
    def update_project(self, project_id, data):
        """Update project details"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            # Validate foreign keys if being updated
            if 'program_id' in data:
                program = Program.query.get(data['program_id'])
                if not program:
                    return jsonify({'error': 'Invalid program_id'}), 400
                    
            if 'facility_id' in data:
                facility = Facility.query.get(data['facility_id'])
                if not facility:
                    return jsonify({'error': 'Invalid facility_id'}), 400
            
            updatable_fields = ['program_id', 'facility_id', 'title', 'nature_of_project',
                              'description', 'innovation_focus', 'prototype_stage',
                              'testing_requirements', 'commercialization_plan']
            for field in updatable_fields:
                if field in data:
                    setattr(project, field, data[field])
            
            db.session.commit()
            return jsonify(project.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update project: {str(e)}'}), 400
    
    def delete_project(self, project_id):
        """Delete project (with dependency checks)"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            # Check for dependencies
            participant_count = ProjectParticipant.query.filter_by(project_id=project_id).count()
            outcome_count = Outcome.query.filter_by(project_id=project_id).count()
            
            dependencies = []
            if participant_count > 0:
                dependencies.append(f'{participant_count} participants')
            if outcome_count > 0:
                dependencies.append(f'{outcome_count} outcomes')
            
            if dependencies:
                return jsonify({
                    'error': f'Cannot delete project. It has {", ".join(dependencies)} linked to it.'
                }), 400
            
            db.session.delete(project)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete project: {str(e)}'}), 500
    
    def assign_participant(self, project_id, data):
        """Assign participant to project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            participant_id = data.get('participant_id')
            if not participant_id:
                return jsonify({'error': 'Missing participant_id'}), 400
                
            participant = Participant.query.get(participant_id)
            if not participant:
                return jsonify({'error': 'Invalid participant_id'}), 400
            
            # Check if already assigned
            existing = ProjectParticipant.query.filter_by(
                project_id=project_id, 
                participant_id=participant_id
            ).first()
            if existing:
                return jsonify({'error': 'Participant already assigned to this project'}), 400
            
            # Create association
            project_participant = ProjectParticipant(
                project_id=project_id,
                participant_id=participant_id,
                role_on_project=data.get('role_on_project', 'Student'),
                skill_role=data.get('skill_role', 'Developer')
            )
            
            db.session.add(project_participant)
            db.session.commit()
            
            return jsonify(project_participant.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to assign participant: {str(e)}'}), 400
    
    def remove_participant(self, project_id, participant_id):
        """Remove participant from project"""
        try:
            project_participant = ProjectParticipant.query.filter_by(
                project_id=project_id,
                participant_id=participant_id
            ).first()
            
            if not project_participant:
                return jsonify({'error': 'Participant not assigned to this project'}), 404
            
            db.session.delete(project_participant)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to remove participant: {str(e)}'}), 500
    
    def get_project_participants(self, project_id):
        """Get all participants for a project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            # Query with join to get participant details
            participants = db.session.query(
                Participant, ProjectParticipant
            ).join(
                ProjectParticipant, Participant.participant_id == ProjectParticipant.participant_id
            ).filter(
                ProjectParticipant.project_id == project_id
            ).all()
            
            result = []
            for participant, project_participant in participants:
                participant_data = participant.to_dict()
                participant_data.update({
                    'role_on_project': project_participant.role_on_project,
                    'skill_role': project_participant.skill_role
                })
                result.append(participant_data)
            
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve participants: {str(e)}'}), 500
    
    def get_project_outcomes(self, project_id):
        """Get all outcomes for a project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            outcomes = Outcome.query.filter_by(project_id=project_id).all()
            return jsonify([outcome.to_dict() for outcome in outcomes]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve outcomes: {str(e)}'}), 500
