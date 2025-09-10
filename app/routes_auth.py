from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from .extensions import db
from .models import User, UserSetting


bp = Blueprint("auth", __name__)


@bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("auth_login.html", title="Entrar")


@bp.post("/login")
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash("Usuário ou senha inválidos.", "danger")
        return redirect(url_for("auth.login"))
    login_user(user)
    flash("Login efetuado.", "success")
    return redirect(url_for("main.index"))


@bp.get("/register")
def register():
    return render_template("auth_register.html", title="Registrar")


@bp.post("/register")
def register_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        flash("Informe usuário e senha.", "warning")
        return redirect(url_for("auth.register"))
    if User.query.filter_by(username=username).first():
        flash("Usuário já existe.", "warning")
        return redirect(url_for("auth.register"))
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    # cria settings padrão
    s = UserSetting(user_id=user.id)
    db.session.add(s)
    db.session.commit()
    flash("Cadastro realizado. Faça login.", "success")
    return redirect(url_for("auth.login"))


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))

