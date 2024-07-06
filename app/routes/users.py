from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import db, User
from app.utils import bcrypt


users_bp = Blueprint("users", __name__)


@users_bp.route("/api/register", methods=["POST"])
def register():
    """
    Register a new user by creating a User object with the provided data.

    Parameters:
        None

    Returns:
        A JSON response indicating the success of user registration.
    """
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
    """
    Logs in a user by checking if the provided username and password match a user in the database.

    Parameters:
        None

    Returns:
        A JSON response containing an access token if the login is successful, or a JSON response with an error message and a status code of 401 if the login is unsuccessful.
    """

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
    """
    Retrieves the current user using the get_jwt_identity function and returns a JSON response containing the current user information along with a status code of 200.
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
