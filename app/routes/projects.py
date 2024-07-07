from typing import Dict
from flask import Blueprint, jsonify, request
from app.models import User, db, Project, Issue
from sqlalchemy.orm import joinedload

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/api/projects", methods=["GET"])
def get_projects():
    user_id: int = request.args.get("user_id")
    if user_id is None:
        return jsonify({"message": "User ID is required"}), 400

    projects = Project.query.filter_by(user_id=user_id).all()

    project_data = [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "issues": [
                {"id": issue.id, "title": issue.title} for issue in project.issues
            ],
        }
        for project in projects
    ]

    return jsonify(project_data), 200


@projects_bp.route("/api/project", methods=["GET"])
def get_project():
    project_id = request.args.get("project_id", type=int)
    user_id = request.args.get("user_id", type=int)
    if not project_id:
        return jsonify({"message": "ID Not Found"}), 404

    if user_id is None:
        return jsonify({"message": "User ID is required"}), 400

    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({"message": "Project Not Found"}), 404

    project_data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "issues": [
            {
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status,
            }
            for issue in project.issues
        ],
    }

    return jsonify(project_data), 200


@projects_bp.route("/api/projects", methods=["POST"])
def create_project():
    data: Dict[str, str | int] = request.get_json()
    user_id: int = data.get("user_id")
    name: str = data.get("name")
    description: str = data.get("description")
    if not (name and description and user_id):
        return jsonify({"message": "Name, description, and user_id are required"}), 400

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_project = Project(
        name=name, description=description, user_id=user_id, issues=[]
    )

    db.session.add(new_project)
    db.session.commit()

    return (
        jsonify({"id": new_project.id, "message": "Project created successfully"}),
        201,
    )


@projects_bp.route("/api/projects", methods=["DELETE"])
def delete_project():
    project_id = request.args.get("id", type=int)
    if not project_id:
        return jsonify({"message": "ID Not Found"}), 404

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"message": "Project Not Found"}), 404

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted successfully"}), 200
