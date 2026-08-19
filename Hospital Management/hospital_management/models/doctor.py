"""Doctor model."""

from models.database import get_connection


class Doctor:
    """Doctor entity."""

    TABLE = "doctors"

    def __init__(self, id=None, name="", specialty="", phone="", email=""):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.phone = phone
        self.email = email

    @staticmethod
    def create(name, specialty, phone, email):
        """Create a new doctor record."""
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO doctors (name, specialty, phone, email) VALUES (?, ?, ?, ?)",
                (name, specialty, phone, email),
            )
            conn.commit()
            return Doctor.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(doctor_id):
        """Get a doctor by ID."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
            return Doctor.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Get all doctors."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM doctors").fetchall()
            return [Doctor.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def update(doctor_id, name, specialty, phone, email):
        """Update an existing doctor."""
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

    @staticmethod
    def from_row(row):
        """Convert a sqlite3.Row to a Doctor object."""
        return Doctor(
            id=row["id"],
            name=row["name"],
            specialty=row["specialty"],
            phone=row["phone"],
            email=row["email"],
        )

    def to_dict(self):
        """Serialise to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "phone": self.phone,
            "email": self.email,
        }