import os
from app.db import get_answers_collection
from app.config import DATA_DIR
from app.utils import read_json_file

answers_collection = get_answers_collection()


def enrich_with_status(data, user_password):
    ids = [str(item["id"]) for item in data if "id" in item]
    if not ids:
        return data

    pipeline = [
        {"$match": {"user_password": user_password, "answers.folder_id": {"$in": ids}}},
        {"$unwind": "$answers"},
        {"$match": {"answers.folder_id": {"$in": ids}}},
        {"$project": {"_id": 0, "folder_id": "$answers.folder_id", "status": "$answers.already_completed"}}
    ]
    status_docs = list(answers_collection.aggregate(pipeline))
    status_map = {d["folder_id"]: d["status"] for d in status_docs}

    for item in data:
        folder_id = str(item.get("id"))
        s = status_map.get(folder_id)
        if s == "false" or s is None:
            item["already_complited"] = False
        elif s == "in_process":
            item["already_complited"] = "in_process"
        elif s is True:
            item["already_complited"] = True
        else:
            item["already_complited"] = False
    return data


def get_limited_data(subject, limit, user_password):
    fp = os.path.join(DATA_DIR, "Sorted_months", subject, "10", "ilich.json")
    if not os.path.exists(fp):
        return None
    try:
        data = read_json_file(fp)
    except Exception:
        return None
    return enrich_with_status(data[-limit:], user_password)
