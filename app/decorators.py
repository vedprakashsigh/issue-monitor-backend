from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Project, Role, User


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user["username"]).first()

            if not user:
                return jsonify({"message": "User not found"}), 403

            if user.role != role and user.role != Role.ADMIN:
                return jsonify({"message": "Permission denied"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def project_access_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id)
        project_id = kwargs.get("project_id")
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"message": "Project not found!"}), 404
        if current_user_id != project.user_id and current_user not in project.members:
            return jsonify({"message": "Access forbidden!"}), 403
        g.project = project
        return fn(*args, **kwargs)

    return decorator
