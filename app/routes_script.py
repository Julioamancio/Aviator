from __future__ import annotations

import os
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from .extensions import db
from .models import UserSetting


bp = Blueprint("script", __name__)


def _user_dir(user_id: int) -> Path:
    base = Path("user_uploads") / str(user_id)
    base.mkdir(parents=True, exist_ok=True)
    return base


@bp.get("/")
@login_required
def view():
    settings: UserSetting = UserSetting.query.filter_by(user_id=current_user.id).first()  # type: ignore[arg-type]
    return render_template("script.html", title="Script", settings=settings)


@bp.post("/save-path")
@login_required
def save_path():
    path = request.form.get("script_path", "").strip()
    if not path:
        flash("Informe um caminho válido.", "warning")
        return redirect(url_for("script.view"))
    s: UserSetting = UserSetting.query.filter_by(user_id=current_user.id).first()  # type: ignore[arg-type]
    if not s:
        s = UserSetting(user_id=current_user.id)
        db.session.add(s)
    s.script_path = path
    db.session.commit()
    flash("Caminho salvo.", "success")
    return redirect(url_for("script.view"))


@bp.post("/upload")
@login_required
def upload():
    f = request.files.get("file")
    if not f or not f.filename.endswith(".py"):
        flash("Envie um arquivo .py.", "warning")
        return redirect(url_for("script.view"))
    base = _user_dir(current_user.id)  # type: ignore[arg-type]
    dest = base / f.filename
    f.save(dest)
    # Atualiza settings para apontar ao arquivo enviado
    s: UserSetting = UserSetting.query.filter_by(user_id=current_user.id).first()  # type: ignore[arg-type]
    if not s:
        s = UserSetting(user_id=current_user.id)
        db.session.add(s)
    s.script_path = str(dest)
    db.session.commit()
    flash("Upload concluído e caminho configurado.", "success")
    return redirect(url_for("script.view"))

