from __future__ import annotations

from datetime import datetime, timedelta, date
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    serial_key = db.Column(db.String(120), nullable=True)
    activation_date = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def license_valid(self) -> bool:
        if not self.activation_date or not self.serial_key:
            return False
        return date.today() <= (self.activation_date + timedelta(days=30))

    def license_days_left(self) -> int:
        if not self.activation_date or not self.serial_key:
            return 0
        delta = (self.activation_date + timedelta(days=30)) - date.today()
        return max(delta.days, 0)


class UserSetting(db.Model):
    __tablename__ = "user_settings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    # Campos simples (evita JSON para facilitar leitura)
    strategy_name = db.Column(db.String(80), default="threshold", nullable=False)
    threshold = db.Column(db.Float, default=1.5, nullable=False)
    risk_percent = db.Column(db.Float, default=2.0, nullable=False)
    max_consecutive_losses = db.Column(db.Integer, default=3, nullable=False)
    script_path = db.Column(db.String(512), default="app/user_script.py", nullable=False)
    interval_seconds = db.Column(db.Float, default=2.0, nullable=False)

    user = db.relationship("User", backref=db.backref("settings", uselist=False))


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None
