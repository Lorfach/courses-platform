import os
from functools import lru_cache
import json
import logging
from app.config import DATA_DIR


@lru_cache(maxsize=256)
def read_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_months_for_user(user, subject, body=None):
    is_math = (body or {}).get("math") == "TRUE" or subject == "math"
    free_user = user.get("free_user", False)
    date_field = "date" if is_math else "date_rus"
    months = user.get(date_field)
    if free_user and not months:
        return ["10"]
    return months or []


def find_question_file(subject, months_from_bd, folder_id, question_id=None):
    base = os.path.join(DATA_DIR, "Sorted_months", subject)
    try:
        months_on_disk = os.listdir(base)
    except FileNotFoundError:
        return None
    for m in months_on_disk:
        if m in months_from_bd:
            if question_id:
                fp = os.path.join(base, m, folder_id, f"{question_id}.json")
            else:
                fp = os.path.join(base, m, folder_id, f"{folder_id}.json")
            if os.path.exists(fp):
                return fp
    return None
