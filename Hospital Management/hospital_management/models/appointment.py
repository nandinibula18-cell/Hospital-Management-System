"""Appointment model."""

from models.database import get_connection


class Appointment:
    """Appointment entity."""

    TABLE = "appointments"

    def __init__(self, id=None, patient_id=None, doctor_id=None, appointment_date="", appointment_time="", status="scheduled", notes=""):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.notes = notes

    @staticmethod
    def create(patient_id, doctor_id, appointment_date, appointment_time, notes=""):
        """Create a new appointment."""
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, notes) VALUES (?, ?, ?, ?, ?)",
                (patient_id, doctor_id, appointment_date, appointment_time, notes),
            )
            conn.commit()
            return Appointment.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(appointment_id):
        """Get an appointment by ID."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
            return Appointment.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_patient(patient_id):
        """Get appointments for a patient."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient_id,)).fetchall()
            return [Appointment.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_doctor(doctor_id):
        """Get appointments for a doctor."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM appointments WHERE doctor_id = ?", (doctor_id,)).fetchall()
            return [Appointment.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def update_status(appointment_id, status):
        """Update appointment status."""
        conn = get_connection()
        try:
            conn.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, appointment_id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def cancel(appointment_id):
        """Cancel an appointment."""
        conn = get_connection()
        try:
            conn.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def from_row(row):
        """Convert a sqlite3.Row to an Appointment object."""
        return Appointment(
            id=row["id"],
            patient_id=row["patient_id"],
            doctor_id=row["doctor_id"],
            appointment_date=row["appointment_date"],
            appointment_time=row["appointment_time"],
            status=row["status"],
            notes=row["notes"],
        )

    def to_dict(self):
        """Serialise to a dictionary."""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
            "status": self.status,
            "notes": self.notes,
        }