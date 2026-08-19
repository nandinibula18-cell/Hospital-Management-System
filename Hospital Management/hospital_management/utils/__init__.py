"""Utilities package."""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in.")
                return redirect(url_for("auth.login"))
            role = session.get("role")
            if role not in roles:
                flash("You do not have permission to access this page.")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)

        return decorated

    return decorator


class ValidationError(Exception):
    pass


def validate_required(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        raise ValidationError(f"Missing fields: {', '.join(missing)}")


def validate_email(email):
    return "@" in email and "." in email


def validate_phone(phone):
    return len(phone) >= 10 and phone.isdigit()