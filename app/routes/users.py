from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import db, User


users_bp = Blueprint("users", __name__)


@users_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        name=data["name"], username=data["username"], email=data["email"], projects=[]
    )
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})


@users_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user: User | None = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={"username": user.username})
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401


@users_bp.route("/api/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user["username"]).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"logged_in_as": current_user, "user_id": user.id}), 200
