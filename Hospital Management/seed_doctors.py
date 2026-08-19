"""Seed the database with 20 doctors."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "instance" / "hospital.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DOCTORS = [
    ("Dr. Aarav Sharma", "Cardiology", "9812345670", "aarav.sharma@hospital.com"),
    ("Dr. Priya Singh", "Neurology", "9823456781", "priya.singh@hospital.com"),
    ("Dr. Vikram Patel", "Orthopedics", "9834567892", "vikram.patel@hospital.com"),
    ("Dr. Ananya Iyer", "Pediatrics", "9845678903", "ananya.iyer@hospital.com"),
    ("Dr. Rohan Gupta", "Dermatology", "9856789014", "rohan.gupta@hospital.com"),
    ("Dr. Meera Nair", "Gynecology", "9867890125", "meera.nair@hospital.com"),
    ("Dr. Kabir Khan", "ENT", "9878901236", "kabir.khan@hospital.com"),
    ("Dr. Ishita Das", "Psychiatry", "9889012347", "ishita.das@hospital.com"),
    ("Dr. Arjun Mehta", "Urology", "9890123458", "arjun.mehta@hospital.com"),
    ("Dr. Divya Menon", "Radiology", "9901234569", "divya.menon@hospital.com"),
    ("Dr. Karthik Nair", "Oncology", "9912345670", "karthik.nair@hospital.com"),
    ("Dr. Shreya Joshi", "Ophthalmology", "9923456781", "shreya.joshi@hospital.com"),
    ("Dr. Aditya Verma", "Gastroenterology", "9934567892", "aditya.verma@hospital.com"),
    ("Dr. Kavya Krishna", "Endocrinology", "9945678903", "kavya.krishna@hospital.com"),
    ("Dr. Lakshmi Narayan", "Pulmonology", "9956789014", "lakshmi.narayan@hospital.com"),
    ("Dr. Sneha Reddy", "Nephrology", "9967890125", "sneha.reddy@hospital.com"),
    ("Dr. Nikhil Verma", "Psychiatry", "9978901236", "nikhil.verma@hospital.com"),
    ("Dr. Pooja Rao", "Hematology", "9989012347", "pooja.rao@hospital.com"),
    ("Dr. Gaurav Sinha", "Surgery", "9990123458", "gaurav.sinha@hospital.com"),
    ("Dr. Neha Kulkarni", "Urology", "9901234569", "neha.kulkarni@hospital.com"),
    ("Dr. Kunal Chopra", "Plastic Surgery", "9912345670", "kunal.chopra@hospital.com"),
    ("Dr. Ritu Agarwal", "Pathology", "9923456781", "ritu.agarwal@hospital.com"),
]

conn = sqlite3.connect(str(DB_PATH))
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'patient',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
        doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'scheduled',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS billings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
        amount REAL NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'unpaid',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)
conn.executemany(
    "INSERT INTO doctors (name, specialty, phone, email) VALUES (?, ?, ?, ?)",
    DOCTORS,
)
conn.commit()
count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
conn.close()

print(f"Seeded {count} doctors into the database at {DB_PATH}")