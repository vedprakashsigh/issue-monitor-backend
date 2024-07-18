from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Comment, User, db


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
    comment_id = request.args.get("comment_id")
    if not comment_id:
        return jsonify({"message": "Comment ID is required"}), 400
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    return (
        jsonify(comment),
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


@comments_bp.route("/api/comments", methods=["POST"])
@jwt_required()
def edit_comment():
    data = request.get_json()
    comment_id = data.get("comment_id")
    if not comment_id:
        return jsonify({"message": "Comment ID is required"}), 400
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment or comment.user_id != user_id:
        return jsonify({"message": "Not authorized or comment not found"}), 403
    comment.content = data.get("content", comment.content)
    db.session.commit()
    return jsonify({"message": "Comment updated successfully"}), 200


@comments_bp.route("/api/comment", methods=["DELETE"])
@jwt_required()
def delete_comment():
    data = request.get_json()
    comment_id = data.get("id")
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment or comment.user_id != user_id:
        return jsonify({"message": "Not authorized or comment not found"}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200
