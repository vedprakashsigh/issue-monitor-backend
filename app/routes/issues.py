from typing import List
from flask import Blueprint, jsonify, request
from app.models import db, Issue

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/api/issues', methods=['GET'])
def get_issues():
    issues:List[Issue] = Issue.query.all()
    return jsonify([{
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.status,
        'project_id': issue.project_id
    } for issue in issues])


@issues_bp.route('/api/issue', methods=['GET'])
def get_issue():
    id = request.args.get('id',type=int)
    if not id:
        return jsonify({'message': 'Id Not Found'}), 404
        
    issue:Issue|None = Issue.query.get(id)
    if not issue:
        return jsonify({'message': 'Issue Not Found'}), 404
        
    return jsonify({
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.status,
        'project_id': issue.project_id
    } )


@issues_bp.route('/api/issues', methods=['POST'])
def create_issue():
    title,description,status,project_id = request.get_json()
    new_issue:Issue = Issue(
        title=title,
        description=description,
        status=status,
        project_id=project_id,
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify({'message': 'Issue created successfully!'}), 200


@issues_bp.route('/api/issues', methods=['DELETE'])
def delete_issue():
    id:int|None = request.args.get('id',type=int)
    if not id:
        return jsonify({'message': 'Id Not Found'}), 404

    issue:Issue|None = Issue.query.get(id)
    if not issue:
        return jsonify({'message': 'Issue Not Found'}), 404

    db.session.delete(issue)
    db.session.commit()
    return jsonify({'message': 'Issue Deleted successfully!'}), 200
