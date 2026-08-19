"""Appointment service - business logic."""

import sqlite3
from models.appointment import Appointment
from models.database import get_connection


class AppointmentService:
    """Appointment business logic."""

    @staticmethod
    def create(patient_id, doctor_id, appointment_date, appointment_time, notes=""):
        """Create a new appointment."""
        return Appointment.create(
            patient_id, doctor_id, appointment_date, appointment_time, notes
        )

    @staticmethod
    def get_by_id(appointment_id):
        """Get appointment by ID."""
        return Appointment.get_by_id(appointment_id)

    @staticmethod
    def get_by_patient(patient_id):
        """Get all appointments for a patient."""
        return Appointment.get_by_patient(patient_id)

    @staticmethod
    def get_by_doctor(doctor_id):
        """Get all appointments for a doctor."""
        return Appointment.get_by_doctor(doctor_id)

    @staticmethod
    def get_all():
        """Get all appointments."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM appointments ORDER BY id DESC").fetchall()
            return [Appointment.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_count():
        """Return the total number of appointments."""
        conn = get_connection()
        try:
            return conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def update_status(appointment_id, status):
        """Update appointment status."""
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE appointments SET status = ? WHERE id = ?",
                (status, appointment_id),
            )
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