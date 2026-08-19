"""Doctor service - business logic for doctor operations."""
from models.database import get_connection
from models.doctor import Doctor


class DoctorService:
    """Business logic for doctor operations."""

    @staticmethod
    def create(name, specialty, phone, email):
        """Create a new doctor record."""
        if not name or not specialty or not phone or not email:
            raise ValueError("All fields are required.")

        if "@" not in email or "." not in email:
            raise ValueError("Please enter a valid email address.")

        if len(phone) < 10:
            raise ValueError("Phone number must be at least 10 digits.")

        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO doctors (name, speciality, phone, email) VALUES (?, ?, ?, ?)",
                (name, specialty, phone, email),
            )
            conn.commit()
            return Doctor.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Get all doctors."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
            return [Doctor.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_count():
        """Return the total number of doctors."""
        conn = get_connection()
        try:
            return conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(doctor_id):
        """Get a doctor by ID."""
        return Doctor.get_by_id(doctor_id)

    @staticmethod
    def update(doctor_id, name, specialty, phone, email):
        """Update a doctor record."""
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE doctors SET name = ?, specialty = ?, phone = ?, email = ? WHERE id = ?",
                (name, specialty, phone, email, doctor_id),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(doctor_id):
        """Delete a doctor."""
        conn = get_connection()
        try:
            conn.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()
        finally:
            conn.close()