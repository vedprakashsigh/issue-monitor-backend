from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import db, User, Role


users_bp = Blueprint("users", __name__)


@users_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([name, username, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    user = User(name=name, username=username, email=email, projects=[])

    # Automatically assign role based on email domain
    if email.endswith("@admin.com"):
        user.role = Role.ADMIN
    elif email.endswith("@manager.com"):
        user.role = Role.PROJECT_MANAGER
    else:
        user.role = Role.DEFAULT_ROLE

    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


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
    return (
        jsonify({"logged_in_as": current_user, "user_id": user.id, "role": user.role}),
        200,
    )


@users_bp.route("/api/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "username": user.username,
        }
        for user in users
    ]
    return jsonify({"users": user_list})
