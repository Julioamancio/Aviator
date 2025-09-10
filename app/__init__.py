import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from .config_manager import ConfigManager
from .bot_service import BotManager
from .extensions import db, login_manager
from .models import User, UserSetting


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # DB
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)

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

    # Serviço do bot (multiusuário simples)
    app.bot_manager = BotManager(app.config_manager)

    # Rotas
    from .routes import bp as main_bp
    from .routes_auth import bp as auth_bp
    from .routes_license import bp as lic_bp
    from .routes_script import bp as script_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(lic_bp, url_prefix="/license")
    app.register_blueprint(script_bp, url_prefix="/script")
    app.register_blueprint(main_bp)

    # Cria tabelas e usuário admin default (opcional)
    with app.app_context():
        db.create_all()
        # Admin default
        from datetime import datetime
        admin_user = User.query.filter_by(username=os.getenv("ADMIN_USERNAME", "admin")).first()
        if not admin_user:
            admin_user = User(username=os.getenv("ADMIN_USERNAME", "admin"), is_admin=True)
            admin_user.set_password(os.getenv("ADMIN_PASSWORD", "admin123"))
            db.session.add(admin_user)
            db.session.commit()
        # Garante settings para usuários existentes
        for user in User.query.all():
            if not user.settings:
                s = UserSetting(user_id=user.id)
                db.session.add(s)
        db.session.commit()

    return app
