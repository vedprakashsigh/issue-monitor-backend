from math import inf
from flask import Blueprint, jsonify, request
from app.models import Log

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    # Get the 'count' query parameter from the request
    count = request.args.get("count", default=inf, type=int)

    # Fetch logs from the database
    logs = Log.query.all()

    # Ensure count is not more than available logs
    if count == inf:
        count = len(logs)
    else:
        count = min(count, len(logs))

    # Return logs in reverse order
    return jsonify(
        [
            {"id": log.id, "action": log.action, "timestamp": log.timestamp}
            for log in logs[-count:][::-1]
        ]
    )
