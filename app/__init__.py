# app/__init__.py

from flask import Flask
from flask_cors import CORS
from app.models import db
from app.routes.issues import issues_bp
from app.routes.projects import projects_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='your_secret_key_here',  # Replace with your own secret key
        SQLALCHEMY_DATABASE_URI='sqlite:///../instance/project.db',  # SQLite database URI
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize SQLAlchemy with Flask app
    db.init_app(app)

    # Enable CORS for all routes
    CORS(app)

    # Register Blueprints
    app.register_blueprint(issues_bp)
    app.register_blueprint(projects_bp)

    return app
