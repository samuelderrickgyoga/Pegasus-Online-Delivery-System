from flask import jsonify
from app.models.program import Program
from app.models.project import Project
from app.database import db

class ProgramController:
    
    def get_all_programs(self):
        """List all programs"""
        try:
            programs = Program.query.all()
            return jsonify([program.to_dict() for program in programs]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve programs: {str(e)}'}), 500
    
    def get_program_by_id(self, program_id):
        """Get program details by ID"""
        try:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'error': 'Program not found'}), 404
            return jsonify(program.to_dict()), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve program: {str(e)}'}), 500
    
    def create_program(self, data):
        """Create new program"""
        try:
            # Validate required fields
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Create new program
            program = Program(
                name=data['name'],
                description=data['description'],
                national_alignment=data.get('national_alignment'),
                focus_areas=data.get('focus_areas'),
                phases=data.get('phases')
            )
            
            db.session.add(program)
            db.session.commit()
            
            return jsonify(program.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create program: {str(e)}'}), 400
    
    def update_program(self, program_id, data):
        """Update program details"""
        try:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'error': 'Program not found'}), 404
            
            # Update fields
            updatable_fields = ['name', 'description', 'national_alignment', 'focus_areas', 'phases']
            for field in updatable_fields:
                if field in data:
                    setattr(program, field, data[field])
            
            db.session.commit()
            return jsonify(program.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update program: {str(e)}'}), 400
    
    def delete_program(self, program_id):
        """Delete program (with dependency check)"""
        try:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'error': 'Program not found'}), 404
            
            # Check for dependent projects
            project_count = Project.query.filter_by(program_id=program_id).count()
            if project_count > 0:
                return jsonify({
                    'error': f'Cannot delete program. {project_count} projects are still linked to this program.'
                }), 400
            
            db.session.delete(program)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete program: {str(e)}'}), 500
    
    def get_projects_by_program(self, program_id):
        """Get all projects under a program"""
        try:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'error': 'Program not found'}), 404
                
            projects = Project.query.filter_by(program_id=program_id).all()
            return jsonify([project.to_dict() for project in projects]), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve projects: {str(e)}'}), 500
