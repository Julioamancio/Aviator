from __future__ import annotations

from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from .extensions import db
from .models import User
from .license_util import verify_license, generate_license


bp = Blueprint("license", __name__)


@bp.get("/")
@login_required
def view():
    return render_template("license.html", title="Licenca", user=current_user)


@bp.post("/activate")
@login_required
def activate():
    serial = request.form.get("serial", "").strip()
    if not serial:
        flash("Informe um serial valido.", "warning")
        return redirect(url_for("license.view"))
    u: User = current_user  # type: ignore
    ok, info = verify_license(current_app.config.get("SECRET_KEY", "dev-secret"), serial, u.username)
    if not ok:
        flash(f"Serial invalido: {info}", "danger")
        return redirect(url_for("license.view"))
    u.serial_key = serial
    u.activation_date = date.today()
    db.session.commit()
    flash("Licenca ativada.", "success")
    return redirect(url_for("license.view"))


@bp.post("/generate")
@login_required
def generate():
    if not getattr(current_user, "is_admin", False):
        flash("Acesso negado.", "danger")
        return redirect(url_for("license.view"))
    username = request.form.get("username", "").strip()
    days = int(request.form.get("days", 30))
    if not username:
        flash("Informe o usuario.", "warning")
        return redirect(url_for("license.view"))
    token = generate_license(current_app.config.get("SECRET_KEY", "dev-secret"), username, days)
    flash(f"Serial gerado para {username}: {token}", "info")
    return redirect(url_for("license.view"))

