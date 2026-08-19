"""Patient model."""

from models.database import get_connection


class Patient:
    """Patient entity."""

    TABLE = "patients"

    def __init__(self, id=None, user_id=None, name="", age=0, gender="", phone="", address=""):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address

    @staticmethod
    def create(user_id, name, age, gender, phone, address=""):
        """Create a new patient record."""
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO patients (user_id, name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, age, gender, phone, address),
            )
            conn.commit()
            return Patient.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(patient_id):
        """Get a patient by ID."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
            return Patient.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """Get patients belonging to a user."""
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM patients WHERE user_id = ?", (user_id,)).fetchall()
            return [Patient.from_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def from_row(row):
        """Convert a sqlite3.Row to a Patient object."""
        return Patient(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            age=row["age"],
            gender=row["gender"],
            phone=row["phone"],
            address=row["address"],
        )

    def to_dict(self):
        """Serialise to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "address": self.address,
        }