import os
from flask import Blueprint, request, jsonify
from app.auth import require_auth, get_user
from app.utils import get_months_for_user, find_question_file, read_json_file
from app.services.content import enrich_with_status, get_limited_data
from app.services.answers import get_user_answers
from app.config import DATA_DIR

content_bp = Blueprint("content", __name__)


@content_bp.route("/api/main_months", methods=["POST"])
@require_auth
def get_months():
    user_password = request.headers.get("password")
    body = request.get_json(silent=True) or {}
    is_math = body.get("math") == "TRUE"
    is_rus = body.get("rus") == "TRUE"
    if not is_math and not is_rus:
        return jsonify({"message": "Выберите предмет (math или rus)"}), 400
    if is_math and is_rus:
        return jsonify({"message": "Выберите только один предмет"}), 400

    user = get_user(user_password, fields=["password", "free_user", "date", "date_rus"])
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404

    subject = "math" if is_math else "rus"
    months = get_months_for_user(user, subject, body)

    free_user = user.get("free_user", False)
    if free_user and not months:
        limited = get_limited_data(subject, 3, user_password)
        if limited is None:
            return jsonify({"message": "Ошибка чтения данных"}), 500
        return jsonify(limited), 200

    folder_path = os.path.join(DATA_DIR, "Sorted_months", subject)
    if not os.path.exists(folder_path):
        return jsonify({"message": f"Папка {folder_path} не найдена"}), 404

    available = []
    for month in (months or []):
        mp = os.path.join(folder_path, month.zfill(2))
        if os.path.isdir(mp):
            available.append(month.zfill(2))
    if not available:
        return jsonify({"message": "Нет доступных папок"}), 404

    combined = []
    for month in sorted(available):
        jp = os.path.join(folder_path, month, "ilich.json")
        try:
            combined.extend(read_json_file(jp))
        except FileNotFoundError:
            continue

    combined = enrich_with_status(combined, user_password)
    return jsonify(combined), 200


@content_bp.route("/api/question_months", methods=["POST"])
@require_auth
def get_questions():
    user_password = request.headers.get("password")
    body = request.get_json(silent=True) or {}
    folder_id = body.get("folder")
    is_math = body.get("math") == "TRUE"
    is_rus = body.get("rus") == "TRUE"

    if not folder_id:
        return jsonify({"message": "Не указан folder ID"}), 400
    if is_math == is_rus:
        return jsonify({"message": "Выберите только один предмет"}), 400

    user = get_user(user_password, fields=["password", "free_user", "date", "date_rus"])
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404

    subject = "math" if is_math else "rus"
    months = get_months_for_user(user, subject, body)

    fp = find_question_file(subject, months, folder_id)
    if not fp:
        return jsonify({"message": "Вам не доступно"}), 403

    try:
        data = read_json_file(fp)
    except Exception:
        return jsonify({"message": "Ошибка чтения файла"}), 500

    return jsonify(data), 200


@content_bp.route("/api/question_inside", methods=["POST"])
@require_auth
def get_questions_inside():
    user_password = request.headers.get("password")
    body = request.get_json(silent=True) or {}
    folder_id = body.get("folder")
    question_id = body.get("question")
    is_math = body.get("math") == "TRUE"

    if not folder_id or not question_id:
        return jsonify({"message": "Не указаны folder или question"}), 400

    user = get_user(user_password, fields=["password", "free_user", "date", "date_rus"])
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404

    subject = "math" if is_math else "rus"
    months = get_months_for_user(user, subject, body)

    fp = find_question_file(subject, months, folder_id, question_id)
    if not fp:
        return jsonify({"message": "Ошибка при исполнении или вам не доступно"}), 403

    try:
        data = read_json_file(fp)
    except Exception:
        return jsonify({"message": "Ошибка чтения файла"}), 500

    answers = get_user_answers(user_password, folder_id, question_id)

    answer_map = {}
    for ans in answers:
        for resp in ans.get("responses", []):
            answer_map[resp["answer_id"]] = resp

    for question in data:
        qid = str(question["id"])
        question["answer2"] = None
        question["correct"] = None
        if qid in answer_map:
            question["answer2"] = answer_map[qid].get("answer")
            question["correct"] = answer_map[qid].get("correct")

    return jsonify(data), 200
