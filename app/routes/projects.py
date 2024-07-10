from typing import Dict
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import User, db, Project


projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/api/projects", methods=["GET"])
@jwt_required()
def get_projects():
    user_id: int | None = request.args.get("user_id", type=int)
    if user_id is None:
        return jsonify({"message": "User ID is required"}), 400

    projects = Project.query.filter_by(user_id=user_id).all()

    project_data = [
        {
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
        for project in projects
    ]

    return jsonify(project_data), 200


@projects_bp.route("/api/project", methods=["GET"])
@jwt_required()
def get_project():
    project_id = request.args.get("project_id", type=int)
    user_id = request.args.get("user_id", type=int)
    if not project_id:
        return jsonify({"message": "ID Not Found"}), 404

    if user_id is None:
        return jsonify({"message": "User ID is required"}), 400

    project = Project.query.filter_by(id=project_id).filter_by(user_id=user_id).first()
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
@jwt_required()
def create_project():
    data: Dict = request.get_json()
    user_id: int | None = data.get("user_id")
    name: str | None = data.get("name")
    description: str | None = data.get("description")
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


@projects_bp.route("/api/projects", methods=["PATCH"])
@jwt_required()
def edit_project():
    data: Dict = request.get_json()
    user_id: int | None = data.get("user_id")
    project_id: int | None = data.get("project_id")
    name: str | None = data.get("name")
    description: str | None = data.get("description")

    if not user_id or not project_id:
        return (
            jsonify({"message": "project_id and user_id are required"}),
            400,
        )

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404

    if name:
        project.name = name
    if description:
        project.description = description

    db.session.commit()

    return (
        jsonify({"id": project.id, "message": "Project updated successfully"}),
        201,
    )


@projects_bp.route("/api/project", methods=["DELETE"])
@jwt_required()
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
