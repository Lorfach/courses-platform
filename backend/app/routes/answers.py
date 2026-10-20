import logging
from flask import Blueprint, request, jsonify
from app.auth import require_auth, get_user
from app.utils import get_months_for_user, find_question_file, read_json_file
from app.services.answers import save_answer, update_completion_status

answers_bp = Blueprint("answers", __name__)


@answers_bp.route("/api/answer_to_bd", methods=["POST"])
@require_auth
def answers_to_bd():
    user_password = request.headers.get("password")
    body = request.get_json(silent=True) or {}

    try:
        folder_id = body["folder"]
        question_id = body["question"]
        answer_id = str(body["answer_id"])
        user_answer = body["answer"]
        is_correct = body["correct"]
        subject = body["subject"]
    except KeyError:
        return jsonify({"message": "Ошибка в запросе"}), 400

    user = get_user(user_password, fields=["password", "free_user", "date", "date_rus"])
    if not user:
        return jsonify({"message": "Пользователь не найден"}), 404

    s = "math" if subject == "math" else "rus"
    months = get_months_for_user(user, s, body)

    fp = find_question_file(s, months, folder_id, question_id)
    if not fp:
        return jsonify({"message": "Вопрос не существует по указанному пути"}), 404

    try:
        question_data = read_json_file(fp)
    except Exception:
        return jsonify({"message": "Ошибка чтения файла"}), 500

    question_ids = [str(q["id"]) for q in question_data]
    if answer_id not in question_ids:
        return jsonify({"message": "answer_id не существует в вопросе"}), 404

    save_answer(user_password, folder_id, question_id, answer_id, user_answer, is_correct)
    update_completion_status(user_password, folder_id, question_id, len(question_ids))

    logging.info(f'{user_password} - ответ: "{user_answer}", верный? {is_correct}, предмет: {subject}')
    return jsonify({"message": "Ответ обновлён"}), 200
