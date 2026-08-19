"""Authentication service - handles registration, login, and session logic."""

import sqlite3
from flask import session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from models.database import get_connection
from models.user import User


class AuthService:
    """Service for user registration and authentication."""

    @staticmethod
    def register(name, email, password, role="patient"):
        """Register a new user. Raises ValueError on validation failure."""
        # Validation
        if not name or not email or not password:
            raise ValueError("All fields are required.")

        if "@" not in email or "." not in email:
            raise ValueError("Please enter a valid email address.")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")

        # Check for existing user
        existing = User.get_by_email(email)
        if existing:
            raise ValueError("An account with this email already exists.")

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")

        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, role),
            )
            conn.commit()
            return User.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def login(email, password):
        """Validate login credentials. Return user or None."""
        if not email or not password:
            return None

        user = User.get_by_email(email)
        if user and user.verify_password(password):
            return user

        return None


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def role_required(*roles):
    """Decorator to require a specific role."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in first.", "error")
                return redirect(url_for("auth.login"))
            role = session.get("role")
            if role not in roles:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("dashboard.index"))
            return f(*args, **kwargs)

        return decorated

    return decorator