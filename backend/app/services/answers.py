from app.db import get_answers_collection

answers_collection = get_answers_collection()


def save_answer(user_password, folder_id, question_id, answer_id, user_answer, is_correct):
    existing = answers_collection.find_one({"user_password": user_password})
    if existing:
        answers = existing.get("answers", [])
        found = False
        for ans in answers:
            if ans["folder_id"] == folder_id and ans["quest_id"] == question_id:
                found = True
                resp_found = False
                for resp in ans.get("responses", []):
                    if resp.get("answer_id") == answer_id:
                        resp["answer"] = user_answer
                        resp["correct"] = is_correct
                        resp_found = True
                        break
                if not resp_found:
                    ans.setdefault("responses", []).append({
                        "answer_id": answer_id, "answer": user_answer, "correct": is_correct
                    })
                break
        if not found:
            answers.append({
                "folder_id": folder_id, "quest_id": question_id,
                "responses": [{"answer_id": answer_id, "answer": user_answer, "correct": is_correct}]
            })
        answers_collection.update_one(
            {"user_password": user_password},
            {"$set": {"answers": answers}}
        )
    else:
        answers_collection.insert_one({
            "user_password": user_password,
            "answers": [{
                "folder_id": folder_id, "quest_id": question_id,
                "responses": [{"answer_id": answer_id, "answer": user_answer, "correct": is_correct}]
            }]
        })


def update_completion_status(user_password, folder_id, question_id, total_questions):
    answered = answers_collection.aggregate([
        {"$match": {"user_password": user_password}},
        {"$unwind": "$answers"},
        {"$match": {"answers.folder_id": folder_id, "answers.quest_id": question_id}},
        {"$project": {"responses": "$answers.responses"}},
        {"$unwind": "$responses"},
        {"$group": {"_id": None, "unique": {"$addToSet": "$responses.answer_id"}}}
    ])
    answered_list = list(answered)
    answered_count = len(answered_list[0]["unique"]) if answered_list else 0

    if answered_count == total_questions:
        status = True
    elif answered_count > 0:
        status = "in_process"
    else:
        status = False

    answers_collection.update_one(
        {"user_password": user_password, "answers.folder_id": folder_id, "answers.quest_id": question_id},
        {"$set": {"answers.$.already_completed": status}}
    )


def get_user_answers(user_password, folder_id, question_id):
    existing_user = answers_collection.find_one(
        {"user_password": user_password},
        {"answers": {"$elemMatch": {"folder_id": folder_id, "quest_id": question_id}}}
    )
    return existing_user.get("answers", []) if existing_user else []
