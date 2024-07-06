from typing import List
from flask import Blueprint, jsonify, request
from app.models import db, Issue


issues_bp = Blueprint("issues", __name__)


@issues_bp.route("/api/issues", methods=["GET"])
def get_issues():
    """
    Retrieves all issues from the database and returns them as a JSON response.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents an issue.
        Each dictionary contains the following keys:
        - 'id': The ID of the issue.
        - 'title': The title of the issue.
        - 'description': The description of the issue.
        - 'status': The status of the issue.
        - 'project_id': The ID of the project the issue belongs to.
    """
    issues: List[Issue] = Issue.query.all()
    return jsonify(
        [
            {
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status,
                "project_id": issue.project_id,
            }
            for issue in issues
        ]
    )


@issues_bp.route("/api/issue", methods=["GET"])
def get_issue():
    """
    Retrieves a specific issue from the database based on the provided ID.
    If the ID is not found, returns a JSON response with 'Id Not Found'.
    If the issue is not found, returns a JSON response with 'Issue Not Found'.

    Returns:
        A JSON response containing the details of the retrieved issue, including:
        - 'id': The ID of the issue.
        - 'title': The title of the issue.
        - 'description': The description of the issue.
        - 'status': The status of the issue.
        - 'project_id': The ID of the project the issue belongs to.
    """
    id = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404

    issue: Issue | None = Issue.query.get(id)
    if not issue:
        return jsonify({"message": "Issue Not Found"}), 404

    return jsonify(
        {
            "id": issue.id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status,
            "project_id": issue.project_id,
        }
    )


@issues_bp.route("/api/issues", methods=["POST"])
def create_issue():
    """
    Creates a new issue in the database based on the provided JSON data.

    Parameters:
        None

    Returns:
        A JSON response containing a message indicating the success of the operation and a status code of 200.
    """
    title, description, status, project_id = request.get_json()
    new_issue: Issue = Issue(
        title=title,
        description=description,
        status=status,
        project_id=project_id,
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify({"message": "Issue created successfully!"}), 200


@issues_bp.route("/api/issues", methods=["DELETE"])
def delete_issue():
    """
    Deletes an issue from the database based on the provided ID.

    Parameters:
        None

    Returns:
        A JSON response containing a message indicating the success of the operation and a status code of 200 if the issue is deleted successfully.
        If the ID is not found, a JSON response with a message 'Id Not Found' and a status code of 404 is returned.
        If the issue is not found, a JSON response with a message 'Issue Not Found' and a status code of 404 is returned.
    """
    id: int | None = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404

    issue: Issue | None = Issue.query.get(id)
    if not issue:
        return jsonify({"message": "Issue Not Found"}), 404

    db.session.delete(issue)
    db.session.commit()
    return jsonify({"message": "Issue Deleted successfully!"}), 200
