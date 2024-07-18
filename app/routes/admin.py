from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import db, User, Role
from app.decorators import role_required


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/api/admin/change_role", methods=["POST"])
@jwt_required()
@role_required("admin")
def change_role():
    data = request.get_json()
    user_id = data.get("user_id")
    new_role = data.get("role")

    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

    if new_role not in [Role.ADMIN, Role.PROJECT_MANAGER, Role.MEMBER]:
        return jsonify({"message": "Invalid role"}), 400

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.role = new_role
    db.session.commit()

    return jsonify({"message": "User role updated successfully"}), 200
