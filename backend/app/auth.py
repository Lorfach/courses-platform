import datetime
from functools import wraps
import jwt
from flask import request, jsonify, current_app
from bson import ObjectId
from app.db import get_users_collection

class _UsersCollectionProxy:
    def __getattr__(self, name):
        return getattr(get_users_collection(), name)
    def __getitem__(self, item):
        return get_users_collection()[item]

users_collection = _UsersCollectionProxy()


def generate_token(user_id):
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=336)
    return jwt.encode(
        {"user_id": str(user_id), "exp": exp},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def decode_token(auth_token):
    auth_token = auth_token.replace("Bearer ", "")
    return jwt.decode(auth_token, current_app.config["SECRET_KEY"], algorithms=["HS256"])


def get_user(user_password, fields=None):
    projection = {f: 1 for f in fields} if fields else None
    return users_collection.find_one({"password": user_password}, projection=projection)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get("token")
        user_password = request.headers.get("password")
        if not auth_token or not user_password:
            return jsonify({"message": "Отсутствует токен или пароль"}), 401
        try:
            decode_token(auth_token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Токен истёк"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Неверный токен"}), 401
        return f(*args, **kwargs)
    return decorated
