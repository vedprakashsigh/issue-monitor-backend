import os
from dotenv import load_dotenv # type: ignore

from flask import Flask
from flask_cors import CORS
from app.models import db
from app.routes.issues import issues_bp
from app.routes.projects import projects_bp


load_dotenv()  # Load environment variables from .env file

def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),  
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),  
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
