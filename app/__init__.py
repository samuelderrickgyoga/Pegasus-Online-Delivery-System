from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ods.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'we try again tomorrow'

    db.init_app(app)


    from app.routes.main import main_bp
    from app.routes.programs import programs_bp
    from app.routes.facilities import facilities_bp
    from app.routes.services import services_bp
    from app.routes.equipment import equipment_bp
    from app.routes.projects import projects_bp
    from app.routes.participants import participants_bp
    from app.routes.outcomes import outcomes_bp


    app.register_blueprint(main_bp)
    app.register_blueprint(programs_bp, url_prefix='/api/programs')
    app.register_blueprint(facilities_bp, url_prefix='/api/facilities')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(equipment_bp, url_prefix='/api/equipment')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(participants_bp, url_prefix='/api/participants')
    app.register_blueprint(outcomes_bp, url_prefix='/api/outcomes')

    with app.app_context():
        db.create_all()

    return app
