# app/routes/issues.py

from flask import Blueprint, jsonify, request
from app.models import db, Issue

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/api/issues', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    return jsonify([{
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.status,
        'project_id': issue.project_id
    } for issue in issues])

@issues_bp.route('/api/issues', methods=['POST'])
def create_issue():
    data = request.get_json()
    new_issue = Issue(
        title=data['title'],
        description=data['description'],
        status=data['status'],
        project_id=data['project_id']
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify({'message': 'Issue created successfully!'})
