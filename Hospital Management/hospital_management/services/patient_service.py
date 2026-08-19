"""Patient service - business logic for patient CRUD."""

from models.patient import Patient
from models.database import get_connection


class PatientService:
    """Business logic for patient operations."""

    @staticmethod
    def create(name, age, gender, phone, address=""):
        """Create a new patient record."""
        if not name or not age or not gender or not phone:
            raise ValueError("All fields are required.")
        if int(age) < 0 or int(age) > 120:
            raise ValueError("Age must be between 0 and 120.")
        if len(phone) < 10:
            raise ValueError("Phone number must be at least 10 digits.")

        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
                (name, int(age), gender, phone, address),
            )
            conn.commit()
            return Patient.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(patient_id):
        """Get a patient by ID."""
        return Patient.get_by_id(patient_id)

    @staticmethod
    def get_all():
        """Get all patients."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
            return [Patient.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_count():
        """Return the total number of patients."""
        conn = get_connection()
        try:
            return conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        """Get all patients belonging to a user."""
        return Patient.get_by_user_id(user_id)

    @staticmethod
    def update(patient_id, name, age, gender, phone, address):
        """Update a patient record."""
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE patients SET name = ?, age = ?, gender = ?, phone = ?, address = ? WHERE id = ?",
                (name, int(age), gender, phone, address, patient_id),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(patient_id):
        """Delete a patient by ID."""
        conn = get_connection()
        try:
            conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
            conn.commit()
        finally:
            conn.close()