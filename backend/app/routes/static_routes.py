import os
from flask import Blueprint, send_from_directory, current_app

static_bp = Blueprint("static", __name__)


@static_bp.route("/", defaults={"path": ""})
@static_bp.route("/<path:path>")
def catch_all(path):
    dist = os.path.join(current_app.root_path, "..", "dist")
    if not path:
        return send_from_directory(dist, "index.html")
    full_path = os.path.join(dist, path)
    if os.path.exists(full_path):
        return send_from_directory(dist, path)
    return send_from_directory(dist, "index.html")
