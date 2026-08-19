"""Billing service - business logic for payments/invoices."""

from models.billing import Billing
from models.database import get_connection


class BillingService:
    """Business logic for billing operations."""

    @staticmethod
    def create(appointment_id, amount, description=""):
        """Create a new billing record."""
        return Billing.create(appointment_id, amount, description)

    @staticmethod
    def get_by_id(billing_id):
        """Get a billing record by ID."""
        return Billing.get_by_id(billing_id)

    @staticmethod
    def get_by_appointment(appointment_id):
        """Get billing records for an appointment."""
        return Billing.get_by_appointment(appointment_id)

    @staticmethod
    def get_all():
        """Get all billing records."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM billings ORDER BY id DESC").fetchall()
            return [Billing.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_total_revenue():
        """Return the total sum of all paid billings."""
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM billings WHERE status = 'paid'"
            ).fetchone()
            return row[0]
        finally:
            conn.close()

    @staticmethod
    def mark_paid(billing_id):
        """Mark a billing record as paid."""
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE billings SET status = 'paid' WHERE id = ?",
                (billing_id,),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(billing_id):
        """Delete a billing record."""
        conn = get_connection()
        try:
            conn.execute("DELETE FROM billings WHERE id = ?", (billing_id,))
            conn.commit()
        finally:
            conn.close()