#__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ods.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'we try again tomorrow'

    db.init_app(app)
    
    #BLUEPRINTS
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
