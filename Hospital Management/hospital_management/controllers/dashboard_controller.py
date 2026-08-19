"""Dashboard routes."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)
from services.auth_service import login_required, role_required
from services.patient_service import PatientService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.billing_service import BillingService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """Main dashboard page - role-aware summary."""
    role = session.get("role")

    patients_count = PatientService.get_count() if role in ("admin", "doctor") else 0
    doctors_count = DoctorService.get_count() if role == "admin" else 0
    appointments_count = AppointmentService.get_count() if role in ("admin", "doctor") else 0
    revenue = BillingService.get_total_revenue() if role == "admin" else 0

    return render_template(
        "dashboard.html",
        role=role,
        patients_count=patients_count,
        doctors_count=doctors_count,
        appointments_count=appointments_count,
        revenue=revenue,
    )