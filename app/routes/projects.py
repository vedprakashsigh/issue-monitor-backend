# app/routes/projects.py

from flask import Blueprint, jsonify, request
from app.models import db, Project, Issue

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'issues': [{'id': issue.id, 'title': issue.title} for issue in project.issues]
    } for project in projects])

@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    new_project = Project(
        name=data['name'],
        description=data['description']
    )
    db.session.add(new_project)
    db.session.commit()

    # Create issues for the project if provided in the request
    if 'issues' in data:
        issue_data = data["issues"]
        new_issue = Issue(
            title=issue_data['title'],
            description=issue_data['description'],
            status=issue_data['status'],
            project_id=new_project.id
        )
        db.session.add(new_issue)
    db.session.commit()

    return jsonify({'message': 'Project created successfully!'})
