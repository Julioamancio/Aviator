from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, url_for, jsonify, flash

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    status = current_app.bot_service.status()
    return render_template("index.html", status=status, title=current_app.config_manager.get("app", {}).get("title", "Aviator Bot"))


@bp.post("/start")
def start():
    current_app.bot_service.start()
    flash("Bot iniciado.", "success")
    return redirect(url_for("main.index"))


@bp.post("/stop")
def stop():
    current_app.bot_service.stop()
    flash("Bot parado.", "warning")
    return redirect(url_for("main.index"))


@bp.get("/config")
def config_get():
    cfg = current_app.config_manager.load()
    return render_template("config.html", cfg=cfg, title="Configuração")


@bp.post("/config")
def config_post():
    data = current_app.config_manager.load()
    # Atualiza campos conhecidos
    data.setdefault("strategy", {})
    data.setdefault("bot", {})
    data["strategy"]["name"] = request.form.get("strategy_name", data["strategy"].get("name"))
    data["strategy"]["threshold"] = _f(request.form.get("threshold"), data["strategy"].get("threshold", 1.5))
    data["strategy"]["risk_percent"] = _f(request.form.get("risk_percent"), data["strategy"].get("risk_percent", 2.0))
    data["strategy"]["max_consecutive_losses"] = int(request.form.get("max_consecutive_losses", data["strategy"].get("max_consecutive_losses", 3)))
    data["bot"]["script_path"] = request.form.get("script_path", data["bot"].get("script_path", "app/user_script.py"))
    data["bot"]["interval_seconds"] = _f(request.form.get("interval_seconds"), data["bot"].get("interval_seconds", 2))
    current_app.config_manager.save(data)
    flash("Configuração salva.", "success")
    return redirect(url_for("main.config_get"))


def _f(val, default):
    try:
        return float(val)
    except Exception:
        return float(default)


@bp.get("/logs")
def logs_view():
    lines = current_app.bot_service.tail_logs(200)
    return render_template("logs.html", lines=lines, title="Logs")


@bp.get("/health")
def health():
    return {"status": "ok"}


@bp.get("/api/status")
def api_status():
    return jsonify(current_app.bot_service.status())


@bp.get("/api/logs")
def api_logs():
    return jsonify({"logs": current_app.bot_service.tail_logs(200)})

