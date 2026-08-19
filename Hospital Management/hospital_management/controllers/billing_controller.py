"""Billing CRUD routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.auth_service import login_required, role_required
from services.billing_service import BillingService

billing_bp = Blueprint("billing", __name__)


@billing_bp.route("/billing")
@login_required
@role_required("admin")
def list():
    """List all billing records."""
    billings = BillingService.get_all()
    return render_template("billing/list.html", billings=billings)


@billing_bp.route("/billing/generate", methods=["GET", "POST"])
@login_required
@role_required("admin")
def generate():
    """Generate a new invoice."""
    if request.method == "POST":
        appointment_id = request.form.get("appointment_id")
        amount = request.form.get("amount")
        description = request.form.get("description", "")

        try:
            BillingService.create(appointment_id, amount, description)
            flash("Invoice generated successfully.", "success")
            return redirect(url_for("billing.list"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("billing/generate.html")


@billing_bp.route("/billing/<int:billing_id>/mark-paid", methods=["POST"])
@login_required
@role_required("admin")
def mark_paid(billing_id):
    """Mark a billing record as paid."""
    try:
        BillingService.mark_paid(billing_id)
        flash("Billing marked as paid.", "success")
    except Exception:
        flash("Failed to mark billing as paid.", "error")
    return redirect(url_for("billing.list"))