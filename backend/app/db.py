import logging
import pymongo
import mongomock
from app.config import Config

_client = None
_db = None

def _connect():
    global _client, _db
    if _db is not None and not getattr(_client, "_is_mock", False):
        return
    try:
        _client = pymongo.MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')
        _client._is_mock = False
        _db = _client["test2"]
        logging.info("Connected to remote MongoDB.")
    except Exception as e:
        is_local = "localhost" in Config.MONGO_URI or "127.0.0.1" in Config.MONGO_URI
        if is_local:
            logging.warning("Local MongoDB not available (%s). Using mongomock fallback.", e)
            _client = mongomock.MongoClient()
            _client._is_mock = True
            _db = _client["test2"]
        else:
            logging.error("Remote MongoDB connection error: %s", e)
            raise


def get_users_collection():
    _connect()
    return _db["With_ID_test_2(11.12)"]


def get_answers_collection():
    _connect()
    return _db["With_ID_Answers_2(11.12)"]


def get_execution_collection():
    _connect()
    return _db["Test_execution"]


def create_indexes():
    get_users_collection().create_index("password", unique=True)
    answers = get_answers_collection()
    answers.create_index("user_password", unique=True)
    answers.create_index("answers.folder_id")
    answers.create_index("answers.quest_id")
