import logging
import re
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.db import create_indexes

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

cache = Cache()
limiter = Limiter(
    get_remote_address,
    default_limits=[Config.RATE_LIMIT],
    storage_uri="memory://"
)


def create_app():
    app = Flask(__name__, static_folder="../dist")
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config.from_object(Config)

    cache.init_app(app)
    CORS(
        app,
        origins=[
            re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"),
        ],
        supports_credentials=True,
    )
    limiter.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.content import content_bp
    from app.routes.answers import answers_bp
    from app.routes import static_routes

    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(static_routes.static_bp)

    with app.app_context():
        create_indexes()

    return app
