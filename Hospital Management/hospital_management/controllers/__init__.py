"""Controllers package - central blueprint registry."""

from flask import Blueprint

# Instantiate blueprints
auth_bp = Blueprint("auth", __name__)
dashboard_bp = Blueprint("dashboard", __name__)
patient_bp = Blueprint("patient", __name__)
doctor_bp = Blueprint("doctor", __name__)
appointment_bp = Blueprint("appointment", __name__)
billing_bp = Blueprint("billing", __name__)