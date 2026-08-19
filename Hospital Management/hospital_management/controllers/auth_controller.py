"""Authentication routes (login, register, logout)."""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
)
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "patient")

        try:
            user = AuthService.register(name, email, password, role)
        except ValueError as e:
            flash(str(e), "error")
            return render_template("auth/register.html")

        session["user_id"] = user.id
        session["role"] = user.role
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = AuthService.login(email, password)
        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            flash("Login successful.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    """Handle user logout."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))