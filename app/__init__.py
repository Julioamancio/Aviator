import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from .config_manager import ConfigManager
from .bot_service import BotService


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # Config manager (JSON em config/config.json)
    app.config_manager = ConfigManager()

    # Logging para logs/app.log
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "app.log")
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5, encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(fmt)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Serviço do bot (placeholder até integrar seu script)
    app.bot_service = BotService(app.config_manager)

    # Rotas
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
