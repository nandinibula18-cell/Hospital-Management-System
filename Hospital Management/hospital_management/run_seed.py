 """Seed the database with 20 patients."""
import sqlite3
import pathlib

DB_PATH = pathlib.Path(__file__).parent / "instance" / "hospital.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

PATIENTS = [
    ("Aarav Sharma", 45, "Male", "9812345670", "12 MG Road, Mumbai"),
    ("Priya Singh", 32, "Female", "9823456781", "45 Linking Road, Delhi"),
    ("Vikram Patel", 58, "Male", "9834567892", "78 Park Street, Kolkata"),
    ("Ananya Iyer", 27, "Female", "9845678903", "23 Lake View, Chennai"),
    ("Rohan Gupta", 40, "Male", "9856789014", "67 Residency Road, Bengaluru"),
    ("Meera Nair", 35, "Female", "9867890125", "89 Hill Road, Hyderabad"),
    ("Kabir Khan", 50, "Male", "9878901236", "234 Broadway, Pune"),
    ("Ishita Das", 29, "Female", "9889012347", "567 Sector 17, Gurugram"),
    ("Arjun Mehta", 38, "Male", "9890123458", "890 Civil Lines, Lucknow"),
    ("Divya Menon", 31, "Female", "9901234569", "123 Beach Road, Kochi"),
    ("Karthik Nair", 44, "Male", "9912345670", "456 Lake View, Bhopal"),
    ("Shreya Joshi", 26, "Female", "9923456781", "789 Rose Villa, Indore"),
    ("Aditya Verma", 42, "Male", "9934567892", "23 Lotus Lane, Nagpur"),
    ("Kavya Krishna", 33, "Female", "9945678903", "56 Paradise Ave, Goa"),
    ("Lakshmi Narayan", 47, "Male", "9956789014", "88 Sunrise Street, Jaipur"),
    ("Sneha Reddy", 28, "Female", "9967890125", "34 Moonlight Colony, Vizag"),
    ("Nikhil Verma", 36, "Male", "9978901236", "78 Green Park, Coimbatore"),
    ("Pooja Rao", 41, "Female", "9989012347", "901 Marine Drive, Kochi"),
    ("Gaurav Sinha", 39, "Male", "9990123458", "67 Ring Road, Ranchi"),
    ("Neha Kulkarni", 30, "Female", "9901234569", "23 Silver Oak, Mysuru"),
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

    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
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
    "INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
    PATIENTS,
)
conn.commit()
count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
conn.close()

print(f"Seeded {count} patients into the database at {DB_PATH}")