from typing import Dict
from flask import Blueprint,  jsonify, request
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


@projects_bp.route('/api/project', methods=['GET'])
def get_project():
    id = request.args.get('id',type=int)
    if not id:
        return jsonify({'message':'Id Not Found'}),404
    
    project = Project.query.get(id)
    if not project:
        return jsonify({'message': 'Project Not Found'}), 404
    
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'issues': [{'id': issue.id, 'title': issue.title} for issue in project.issues]})

@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    data:Dict = request.get_json()
    name:str = data.get("name") or ""
    description:str = data.get("description") or ""
    new_project:Project = Project(
        name=name,
        description=description,
        issues=[]
    )
    db.session.add(new_project)
    db.session.commit()

    # Create issues for the project if provided in the request
    if 'issues' in data:
        for issue in data['issues']:            
            new_issue = Issue(
                title=issue['title'],
                description=issue['description'],
                status=issue['status'],
                project_id=new_project.id
            )
            db.session.add(new_issue)
    db.session.commit()

    return jsonify({'message': 'Project created successfully!'})

@projects_bp.route('/api/projects', methods=['DELETE'])
def delete_project():
    id = request.args.get('id',type=int)
    if not id:
        return jsonify({'message': 'Id Not Found'}), 404

    project:Project|None = Project.query.get(id)
    if not project:
        return jsonify({'message': 'Project Not Found'}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project Deleted successfully!'}), 200

