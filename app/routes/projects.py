from typing import Dict
from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Role, User, db, Project
from app.decorators import project_access_required, role_required


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
            "members": [member.id for member in project.members],
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


@projects_bp.route("/api/projects/<int:project_id>/users", methods=["GET"])
@jwt_required()
def get_users(project_id):

    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404
    member_data = {
        "members": [member for member in project.members],
    }

    return jsonify(member_data), 200


@projects_bp.route("/api/project/<int:project_id>", methods=["GET"])
@project_access_required
def get_project(project_id):
    project = g.project
    return (
        jsonify(
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "members": [member.id for member in project.members],
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
        ),
        200,
    )


@projects_bp.route("/api/projects", methods=["POST"])
@jwt_required()
@role_required("project_manager")
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
        name=name, description=description, user_id=user_id, members=[user]
    )

    db.session.add(new_project)
    db.session.commit()

    return (
        jsonify({"id": new_project.id, "message": "Project created successfully"}),
        201,
    )


@projects_bp.route("/api/projects", methods=["PATCH"])
@jwt_required()
@role_required("project_manager")
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
@role_required("admin")
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


@projects_bp.route("/api/projects/<int:project_id>/add_user", methods=["POST"])
@jwt_required()
def add_user_to_project(project_id):
    current_user_username = get_jwt_identity()
    current_user = User.query.filter_by(
        username=current_user_username["username"]
    ).first()
    if not current_user:
        return jsonify({"message": "User not found!"}), 404

    # Check if the current user is an admin or the project manager
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"message": "Project not found!"}), 404
    if (
        current_user.role not in [Role.ADMIN, Role.PROJECT_MANAGER]
        and project.user_id != current_user.id
    ):
        return jsonify({"message": "Access forbidden!"}), 403

    data = request.get_json()
    user_id = data.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found!"}), 404

    if user not in project.members:
        project.members.append(user)
        db.session.commit()
        return jsonify({"message": "User added to project!"}), 200
    else:
        return jsonify({"message": "User is already a member of the project!"}), 400
