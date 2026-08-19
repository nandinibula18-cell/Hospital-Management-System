"""Doctor CRUD routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.auth_service import login_required, role_required
from services.doctor_service import DoctorService

doctor_bp = Blueprint("doctor", __name__)


@doctor_bp.route("/doctors")
@login_required
@role_required("admin")
def list():
    """List all doctors."""
    doctors = DoctorService.get_all()
    return render_template("doctors/list.html", doctors=doctors)


@doctor_bp.route("/doctors/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add():
    """Add a new doctor."""
    if request.method == "POST":
        name = request.form.get("name")
        specialty = request.form.get("specialty")
        phone = request.form.get("phone")
        email = request.form.get("email")

        try:
            DoctorService.create(name, specialty, phone, email)
            flash("Doctor added successfully.", "success")
            return redirect(url_for("doctor.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("doctors/add.html")


@doctor_bp.route("/doctors/<int:doctor_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit(doctor_id):
    """Edit an existing doctor."""
    doctor = DoctorService.get_by_id(doctor_id)
    if not doctor:
        flash("Doctor not found.", "error")
        return redirect(url_for("doctor.list"))

    if request.method == "POST":
        name = request.form.get("name")
        specialty = request.form.get("specialty")
        phone = request.form.get("phone")
        email = request.form.get("email")

        try:
            DoctorService.update(doctor_id, name, specialty, phone, email)
            flash("Doctor updated successfully.", "success")
            return redirect(url_for("doctor.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("doctors/edit.html", doctor=doctor)


@doctor_bp.route("/doctors/<int:doctor_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete(doctor_id):
    """Delete a doctor."""
    try:
        DoctorService.delete(doctor_id)
        flash("Doctor deleted successfully.", "success")
    except Exception:
        flash("Failed to delete doctor.", "error")
    return redirect(url_for("doctor.list"))