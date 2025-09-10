from __future__ import annotations

from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .extensions import db
from .models import User


bp = Blueprint("license", __name__)


@bp.get("/")
@login_required
def view():
    return render_template("license.html", title="Licença", user=current_user)


@bp.post("/activate")
@login_required
def activate():
    serial = request.form.get("serial", "").strip()
    if not serial:
        flash("Informe um serial válido.", "warning")
        return redirect(url_for("license.view"))
    u: User = current_user  # type: ignore
    u.serial_key = serial
    u.activation_date = date.today()
    db.session.commit()
    flash("Licença ativada por 30 dias.", "success")
    return redirect(url_for("license.view"))

