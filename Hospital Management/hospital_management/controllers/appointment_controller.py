"""Appointment CRUD routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.auth_service import login_required, role_required
from services.appointment_service import AppointmentService

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/appointments")
@login_required
@role_required("admin", "doctor")
def list():
    """List all appointments."""
    appointments = AppointmentService.get_all()
    return render_template("appointments/list.html", appointments=appointments)


@appointment_bp.route("/appointments/book", methods=["GET", "POST"])
@login_required
@role_required("admin", "doctor")
def book():
    """Book an appointment."""
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        doctor_id = request.form.get("doctor_id")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")
        notes = request.form.get("notes", "")

        try:
            AppointmentService.create(patient_id, doctor_id, appointment_date, appointment_time, notes)
            flash("Appointment booked successfully.", "success")
            return redirect(url_for("appointment.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("appointments/book.html")


@appointment_bp.route("/appointments/<int:appointment_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "doctor")
def edit(appointment_id):
    """Edit an appointment."""
    appointment = AppointmentService.get_by_id(appointment_id)
    if not appointment:
        flash("Appointment not found.", "error")
        return redirect(url_for("appointment.list"))

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        doctor_id = request.form.get("doctor_id")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")
        status = request.form.get("status")
        notes = request.form.get("notes", "")

        try:
            AppointmentService.update(
                appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, notes
            )
            flash("Appointment updated successfully.", "success")
            return redirect(url_for("appointment.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("appointments/edit.html", appointment=appointment)


@appointment_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@login_required
@role_required("admin", "doctor")
def cancel(appointment_id):
    """Cancel an appointment."""
    try:
        AppointmentService.cancel(appointment_id)
        flash("Appointment cancelled.", "success")
    except Exception:
        flash("Failed to cancel appointment.", "error")
    return redirect(url_for("appointment.list"))