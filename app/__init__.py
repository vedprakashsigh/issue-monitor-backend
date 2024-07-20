import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.routes.issues import issues_bp
from app.routes.projects import projects_bp
from app.routes.users import users_bp
from app.routes.admin import admin_bp
from app.routes.comments import comments_bp
from app.routes.logs import logs_bp
from app.extentions import jwt, bcrypt,  db
import app.listeners

load_dotenv()


def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )

    # Initialize SQLAlchemy with Flask app
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize bcrypt with the app instance
    bcrypt.init_app(app)

    # Initialize jwt with the app instance
    jwt.init_app(app)


    # Enable CORS for all routes
    CORS(app)

    # Register Blueprints
    app.register_blueprint(issues_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(logs_bp)

    return app
