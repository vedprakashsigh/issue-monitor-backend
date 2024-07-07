from typing import List
from flask import Blueprint, jsonify, request
from app.models import db, Issue


issues_bp = Blueprint("issues", __name__)


@issues_bp.route("/api/issues", methods=["GET"])
def get_issues():
    project_id = request.args.get("project_id", type=int)
    if not project_id:
        return jsonify({"message": "Project Id Not Found"}), 404

    issues: Issue | None = Issue.query.filter_by(project_id=project_id).first()
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
    project_id = request.args.get("project_id", type=int)
    id = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404
    if not project_id:
        return jsonify({"message": "Project Id Not Found"}), 404

    issue: Issue | None = Issue.query.filter(
        Issue.id == id and Issue.project_id == project_id
    ).first()
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
    title, description, status, project_id = request.get_json().values()

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
    id: int | None = request.args.get("id", type=int)
    if not id:
        return jsonify({"message": "Id Not Found"}), 404

    issue: Issue | None = Issue.query.filter_by(id=id).first()
    if not issue:
        return jsonify({"message": "Issue Not Found"}), 404

    db.session.delete(issue)
    db.session.commit()
    return jsonify({"message": "Issue Deleted successfully!"}), 200
