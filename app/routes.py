from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required, current_user
from .models import UserSetting

bp = Blueprint("main", __name__)


@bp.get("/")
@login_required
def index():
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    status = svc.status()
    return render_template("index.html", status=status, title=current_app.config_manager.get("app", {}).get("title", "Aviator Bot"))


@bp.post("/start")
@login_required
def start():
    if not current_user.license_valid():  # type: ignore[attr-defined]
        flash("Licenca invalida ou expirada. Ative em Licenca.", "danger")
        return redirect(url_for("license.view"))
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    svc.start()
    flash("Bot iniciado.", "success")
    return redirect(url_for("main.index"))


@bp.post("/stop")
@login_required
def stop():
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    svc.stop()
    flash("Bot parado.", "warning")
    return redirect(url_for("main.index"))


@bp.get("/config")
@login_required
def config_get():
    # Mostra config combinada: global + por usuario
    cfg = current_app.config_manager.load()
    s: UserSetting | None = UserSetting.query.filter_by(user_id=current_user.id).first()  # type: ignore[arg-type]
    return render_template("config.html", cfg=cfg, settings=s, title="Configuracao")


@bp.post("/config")
@login_required
def config_post():
    data = current_app.config_manager.load()
    # Atualiza campos conhecidos
    data.setdefault("strategy", {})
    data.setdefault("bot", {})
    data.setdefault("platform", {})
    # Plataforma (globais)
    data["platform"]["login_url"] = request.form.get("login_url", data["platform"].get("login_url", ""))
    data["platform"]["game_url"] = request.form.get("game_url", data["platform"].get("game_url", ""))
    # Estrategia
    data["strategy"]["name"] = request.form.get("strategy_name", data["strategy"].get("name"))
    data["strategy"]["threshold"] = _f(request.form.get("threshold"), data["strategy"].get("threshold", 1.5))
    data["strategy"]["risk_percent"] = _f(request.form.get("risk_percent"), data["strategy"].get("risk_percent", 2.0))
    data["strategy"]["max_consecutive_losses"] = int(request.form.get("max_consecutive_losses", data["strategy"].get("max_consecutive_losses", 3)))
    data["bot"]["interval_seconds"] = _f(request.form.get("interval_seconds"), data["bot"].get("interval_seconds", 2))
    current_app.config_manager.save(data)

    # Atualiza settings do usuario
    s = UserSetting.query.filter_by(user_id=current_user.id).first()  # type: ignore[arg-type]
    if not s:
        s = UserSetting(user_id=current_user.id)
        db = __import__('app.extensions').extensions.db  # lazy import to avoid cycle
        db.session.add(s)
        db.session.commit()
    s.strategy_name = data["strategy"]["name"]
    s.threshold = float(data["strategy"]["threshold"])
    s.risk_percent = float(data["strategy"]["risk_percent"])
    s.max_consecutive_losses = int(data["strategy"]["max_consecutive_losses"])
    # Credenciais do cliente
    s.platform_username = request.form.get("platform_username", s.platform_username or "")
    s.platform_password = request.form.get("platform_password", s.platform_password or "")
    s.headless = bool(request.form.get("headless"))
    __import__('app.extensions').extensions.db.session.commit()
    flash("Configuracao salva.", "success")
    return redirect(url_for("main.config_get"))


def _f(val, default):
    try:
        return float(val)
    except Exception:
        return float(default)


@bp.get("/logs")
@login_required
def logs_view():
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    lines = svc.tail_logs(200)
    return render_template("logs.html", lines=lines, title="Logs")


@bp.get("/health")
def health():
    return {"status": "ok"}


@bp.get("/api/status")
@login_required
def api_status():
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    return jsonify(svc.status())


@bp.get("/api/logs")
@login_required
def api_logs():
    svc = current_app.bot_manager.get_service(current_user.id)  # type: ignore[arg-type]
    return jsonify({"logs": svc.tail_logs(200)})


# Admin dashboard
@bp.get("/admin")
@login_required
def admin():
    if not getattr(current_user, "is_admin", False):
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))
    from .models import User
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin.html", users=users, title="Admin")

