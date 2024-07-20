from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Comment, User, db
from app.decorators import role_required


comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/api/comments", methods=["GET"])
@jwt_required()
def get_comments():
    issue_id = request.args.get("issue_id")
    if not issue_id:
        return jsonify({"message": "Issue ID is required"}), 400
    comments = Comment.query.filter_by(issue_id=issue_id).all()
    return (
        jsonify(
            [
                {
                    "id": comment.id,
                    "content": comment.content,
                    "user_id": comment.user_id,
                    "issue_id": comment.issue_id,
                    "timestamp": comment.timestamp,
                }
                for comment in comments
            ]
        ),
        200,
    )


@comments_bp.route("/api/comment", methods=["GET"])
@jwt_required()
def get_comment():
    id = request.args.get("id")
    if not id:
        return jsonify({"message": "Comment ID is required"}), 400
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    return (
        jsonify(
            {
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.user_id,
                "issue_id": comment.issue_id,
                "timestamp": comment.timestamp,
            }
        ),
        200,
    )


@comments_bp.route("/api/comments", methods=["POST"])
@jwt_required()
def add_comment():
    data = request.get_json()
    user_id = data.get("user_id")
    issue_id = data.get("issue_id")
    if not issue_id or not user_id:
        return jsonify({"message": "Issue ID and user ID are required"}), 400

    content = data.get("content")
    if not content:
        return jsonify({"message": "Content is required"}), 400
    comment = Comment(content=content, user_id=user_id, issue_id=issue_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully"}), 201


@comments_bp.route("/api/comment", methods=["PATCH"])
@jwt_required()
def edit_comment():
    data = request.get_json()
    id = request.args.get("id")
    if not id:
        return jsonify({"message": "Comment ID is required"}), 400
    jwt = get_jwt_identity()
    username = jwt["username"]
    user = User.query.filter_by(username=username).first()
    comment = Comment.query.filter_by(id=id).first()
    if (
        not user
        or not comment
        or (comment.user_id != user.id and user.role == "member")
    ):
        return jsonify({"message": "Not authorized or comment not found"}), 403
    comment.content = data.get("content", comment.content) or ""
    db.session.commit()
    return jsonify({"message": "Comment updated successfully"}), 200


@comments_bp.route("/api/comment", methods=["DELETE"])
@jwt_required()
def delete_comment():
    id = request.args.get("id")
    jwt = get_jwt_identity()
    username = jwt["username"]
    user = User.query.filter_by(username=username).first()
    comment = Comment.query.filter_by(id=id).first()
    if not user or not comment:
        return jsonify({"message": "Not authorized or comment not found"}), 403
    user_id = user.id
    if not comment or (comment.user_id != user_id and user.role == "member"):
        return jsonify({"message": "Not authorized or comment not found"}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200
