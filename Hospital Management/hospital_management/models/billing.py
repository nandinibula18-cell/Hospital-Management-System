"""Billing model."""

from models.database import get_connection


class Billing:
    """Billing entity."""

    TABLE = "billings"

    def __init__(self, id=None, appointment_id=None, amount=0.0, description="", status="unpaid"):
        self.id = id
        self.appointment_id = appointment_id
        self.amount = amount
        self.description = description
        self.status = status

    @staticmethod
    def create(appointment_id, amount, description=""):
        """Create a new billing record."""
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO billings (appointment_id, amount, description, status) VALUES (?, ?, ?, ?)",
                (appointment_id, amount, description, "unpaid"),
            )
            conn.commit()
            return Billing.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(billing_id):
        """Get a billing record by ID."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM billings WHERE id = ?", (billing_id,)).fetchone()
            return Billing.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_appointment(appointment_id):
        """Get billing records for an appointment."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM billings WHERE appointment_id = ?", (appointment_id,)).fetchall()
            return [Billing.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def mark_paid(billing_id):
        """Mark a billing record as paid."""
        conn = get_connection()
        try:
            conn.execute("UPDATE billings SET status = 'paid' WHERE id = ?", (billing_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def from_row(row):
        """Convert a sqlite3.Row to a Billing object."""
        return Billing(
            id=row["id"],
            appointment_id=row["appointment_id"],
            amount=row["amount"],
            description=row["description"],
            status=row["status"],
        )

    def to_dict(self):
        """Serialise to a dictionary."""
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "amount": self.amount,
            "description": self.description,
            "status": self.status,
        }