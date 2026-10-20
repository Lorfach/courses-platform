import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/courses")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    RATE_LIMIT = "70 per minute"
    CACHE_TYPE = "SimpleCache"
