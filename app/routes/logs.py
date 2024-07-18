from flask import Blueprint, jsonify

from app.models import Log


logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/api/logs/<int:count>", methods=["GET"])
def get_logs(count):
    logs = Log.query.all()
    return jsonify(
        [
            {"id": log.id, "action": log.action, "timestamp": log.timestamp}
            for log in logs[: min(count, len(logs))]
        ]
    )
