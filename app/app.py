import os
from flask import Flask
from config import Config
from app.database import create_database
from app.routes import api_bp
from utils.helpers import ensure_directories_exist

def create_app():
    ensure_directories_exist()
    create_database()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.config.from_object(Config)

    # Register routes blueprint
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)