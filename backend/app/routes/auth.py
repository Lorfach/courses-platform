from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.auth import require_auth, generate_token, decode_token, get_user, users_collection
from app.config import Config
from app import limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
@limiter.limit(Config.RATE_LIMIT)
def login():
    data = request.get_json(silent=True) or {}
    user_password = data.get("password")
    if not user_password or len(str(user_password)) > 50:
        return jsonify({"message": "Пользователь не найден"}), 404
    user = users_collection.find_one({"password": user_password}, {"_id": 1})
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404
    return jsonify({"token": generate_token(user["_id"])}), 200


@auth_bp.route("/api/protected", methods=["GET"])
@require_auth
def protected():
    auth_token = request.headers.get("token", "").replace("Bearer ", "")
    decoded = decode_token(auth_token)
    user = users_collection.find_one({"_id": ObjectId(decoded["user_id"])}, {"_id": 1})
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404
    return jsonify({"message": "Good access", "user_id": str(user["_id"])}), 200


@auth_bp.route("/api/access_to_courses", methods=["POST"])
@require_auth
def get_all_that_they_have():
    user_password = request.headers.get("password")
    user = get_user(user_password, fields=["password", "free_user", "date", "date_rus"])
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 200
    if user.get("free_user", False):
        return jsonify(["math", "rus"])
    data = []
    if user.get("date"):
        data.append("math")
    if user.get("date_rus"):
        data.append("rus")
    return jsonify(data)
