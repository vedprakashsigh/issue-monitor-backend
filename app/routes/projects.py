from typing import Dict
from flask import Blueprint, jsonify, request
from app.models import User, db, Project, Issue


projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/api/projects", methods=["GET"])
def get_projects():
    """
    Get all projects and their associated issues.

    Returns:
        A JSON response containing a list of dictionaries, each representing a project. Each dictionary contains the following keys:
            - 'id': The ID of the project.
            - 'name': The name of the project.
            - 'description': The description of the project.
            - 'issues': A list of dictionaries representing the issues associated with the project. Each dictionary contains the following keys:
                - 'id': The ID of the issue.
                - 'title': The title of the issue.
    """
    projects = Project.query.all()
    return jsonify(
        [
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
    )


@projects_bp.route("/api/project", methods=["GET"])
def get_project():
    """
    Get a project by its ID.

    This function is a route handler for the '/api/project' endpoint with the HTTP method GET. It retrieves a project by its ID from the database and returns it as a JSON response. If the ID is not provided or the project is not found, it returns a JSON response with an appropriate error message and a 404 status code.

    Parameters:
        None

    Returns:
        A JSON response containing the details of the project, including:
            - 'id': The ID of the project.
            - 'name': The name of the project.
            - 'description': The description of the project.
            - 'issues': A list of dictionaries representing the issues associated with the project. Each dictionary contains the following keys:
                - 'id': The ID of the issue.
                - 'title': The title of the issue.

        If the ID is not found or the project is not found, it returns a JSON response with an error message and a 404 status code.
    """
    id = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404

    project = Project.query.filter_by(id=id).first()
    if not project:
        return jsonify({"message": "Project Not Found"}), 404

    return jsonify(
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "issues": [
                {"id": issue.id, "title": issue.title} for issue in project.issues
            ],
        }
    )


@projects_bp.route("/api/projects", methods=["POST"])
def create_project():
    """
    Creates a new project in the database based on the provided JSON data.

    Parameters:
        None

    Returns:
        A JSON response containing a message indicating the success of the operation and a status code of 200.
    """
    data: Dict = request.get_json()
    name: str = data.get("name") or ""
    description: str = data.get("description") or ""
    user_id: int | None = data.get("user") or None
    if not user_id:
        return jsonify({"message": "User Id Not Found"}), 404

    # Create new project
    new_project: Project = Project(
        name=name, description=description, issues=[], user_id=user_id
    )

    user: User | None = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User Not Found"}), 404

    user.projects.append(new_project)

    db.session.add(new_project)
    db.session.add(user)
    db.session.commit()

    # Create issues for the project if provided in the request
    if "issues" in data:
        for issue in data["issues"]:
            new_issue = Issue(
                title=issue["title"],
                description=issue["description"],
                status=issue["status"],
                project_id=new_project.id,
            )
            db.session.add(new_issue)
    db.session.commit()

    return jsonify({"message": "Project created successfully!"})


@projects_bp.route("/api/projects", methods=["DELETE"])
def delete_project():
    """
    Deletes a project from the database based on the provided ID.

    Parameters:
        None

    Returns:
        A JSON response with a message indicating the success of the operation and a status code of 200.
        If the ID is not found or the project is not found, it returns a JSON response with an error message and a status code of 404.
    """
    id = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404

    project: Project | None = Project.query.filter_by(id=id).first()
    if not project:
        return jsonify({"message": "Project Not Found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project Deleted successfully!"}), 200
