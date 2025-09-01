from flask import Flask
from flask_cors import CORS
from routes.programs import programs_bp
from routes.facilities import facilities_bp
from routes.services import services_bp
from routes.equipment import equipment_bp
from routes.projects import projects_bp
from routes.participants import participants_bp
from routes.outcomes import outcomes_bp
# from routes.project_participants import project_participants_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app integration

# Register all blueprints with API prefix
app.register_blueprint(programs_bp, url_prefix='/api/programs')
app.register_blueprint(facilities_bp, url_prefix='/api/facilities')
app.register_blueprint(services_bp, url_prefix='/api/services')
app.register_blueprint(equipment_bp, url_prefix='/api/equipment')
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(participants_bp, url_prefix='/api/participants')
app.register_blueprint(outcomes_bp, url_prefix='/api/outcomes')
# app.register_blueprint(project_participants_bp, url_prefix='/api/project-participants')

if __name__ == '__main__':
    app.run(debug=True)