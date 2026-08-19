"""User model for authentication."""

from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_connection


class User:
    """User entity representing a system user (admin, doctor, patient)."""

    TABLE = "users"

    def __init__(self, id=None, name="", email="", password_hash="", role="patient"):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def create(name, email, password, role="patient"):
        """Create a new user record."""
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (name, email, generate_password_hash(password, method="pbkdf2:sha256"), role),
            )
            conn.commit()
            return User.get_by_id(cursor.lastrowid)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """Retrieve a user by ID."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return User.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        """Retrieve a user by email."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return User.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def from_row(row):
        """Convert a sqlite3.Row to a User object."""
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"],
        )

    def verify_password(self, password):
        """Check password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialise the user to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }