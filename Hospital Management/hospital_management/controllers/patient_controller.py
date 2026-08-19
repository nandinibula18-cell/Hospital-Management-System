"""Patient CRUD routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.auth_service import login_required, role_required
from services.patient_service import PatientService

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/patients")
@login_required
@role_required("admin", "doctor")
def list():
    """List all patients."""
    patients = PatientService.get_all()
    return render_template("patients/list.html", patients=patients)


@patient_bp.route("/patients/add", methods=["GET", "POST"])
@login_required
@role_required("admin", "doctor")
def add():
    """Add a new patient."""
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        address = request.form.get("address", "")

        try:
            PatientService.create(name, age, gender, phone, address)
            flash("Patient added successfully.", "success")
            return redirect(url_for("patient.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("patients/add.html")


@patient_bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "doctor")
def edit(patient_id):
    """Edit an existing patient."""
    patient = PatientService.get_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for("patient.list"))

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        address = request.form.get("address", "")

        try:
            PatientService.update(patient_id, name, age, gender, phone, address)
            flash("Patient updated successfully.", "success")
            return redirect(url_for("patient.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("patients/edit.html", patient=patient)


@patient_bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete(patient_id):
    """Delete a patient."""
    try:
        PatientService.delete(patient_id)
        flash("Patient deleted successfully.", "success")
    except Exception:
        flash("Failed to delete patient.", "error")
    return redirect(url_for("patient.list"))