"""Generate static files, requirements.txt, and README for the project."""
import pathlib

ROOT = pathlib.Path(__file__).parent / "hospital_management"

css = """body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: 600;
}

.table {
    vertical-align: middle;
}

.badge {
    font-size: 0.85rem;
}

.card {
    border-radius: 0.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn {
    border-radius: 0.35rem;
}
"""

js = """// Hospital Management System - client-side enhancements
console.log('Hospital Management System loaded.');

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (el) {
            el.style.transition = 'opacity 0.5s';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 500);
        });
    }, 4000);
});
"""

requirements = """Flask==3.0.3
Werkzeug==3.0.3
"""

readme = """# Hospital Management System

A production-ready web-based **Hospital Management System** built with Python (Flask), SQLite, and Bootstrap. This project demonstrates clean MVC architecture, authentication, role-based access control, full CRUD operations, input validation, and exception handling.

---

## Features

- **Authentication & Authorization**
  - Secure registration and login with password hashing (Werkzeug)
  - Role-based access control: Admin, Doctor, Patient
  - Session-based authentication with `@login_required` and `@role_required` decorators

- **CRUD Operations**
  - Patients: Add, list, edit, delete
  - Doctors: Add, list, edit, delete
  - Appointments: Book, list, update status, cancel
  - Billing: Generate invoice, mark paid

- **Input Validation**
  - Server-side validation (email format, phone length, required fields)
  - Client-side HTML5 validation in forms

- **Exception Handling**
  - Custom `ValidationError` exceptions
  - Graceful error messages using Flask flash

- **OOP Architecture**
  - Models: User, Patient, Doctor, Appointment, Billing
  - Services: Business logic layer
  - Controllers: Flask blueprints (routes)
  - Utils: Decorators, validators

- **Database Integration**
  - SQLite (no setup required)
  - Schema auto-created on first run
  - Seed data for default admin user

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone <your-github-repo-url>
cd hospital_management

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate the environment
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py

# 6. Open the browser at http://localhost:5000
```

### Default Admin Login

| Field | Value |
|-------|-------|
| Email | `admin@hospital.com` |
| Password | `admin123` |

---

## Project Structure

```
hospital_management/
├── app.py                    # Flask application factory
├── config.py                 # Configuration constants
├── requirements.txt          # Dependencies
├── models/                   # Data layer (OOP classes)
│   ├── database.py           # SQLite connection & schema
│   ├── user.py               # User model
│   ├── patient.py            # Patient model
│   ├── doctor.py             # Doctor model
│   ├── appointment.py        # Appointment model
│   └── billing.py            # Billing model
├── services/                 # Business logic layer
│   ├── auth_service.py       # Registration & login
│   ├── patient_service.py    # Patient operations
│   ├── doctor_service.py     # Doctor operations
│   ├── appointment_service.py# Appointment operations
│   └── billing_service.py    # Billing operations
├── controllers/              # Flask blueprints (routes)
│   ├── auth_controller.py    # /login, /register, /logout
│   ├── dashboard_controller.py # Dashboard
│   ├── patient_controller.py # CRUD for patients
│   ├── doctor_controller.py  # CRUD for doctors
│   ├── appointment_controller.py # CRUD for appointments
│   └── billing_controller.py # CRUD for billing
├── utils/                    # Helpers & decorators
│   └── __init__.py           # login_required, role_required, validators
├── templates/                # HTML templates (Jinja2)
│   ├── base.html             # Layout & navbar
│   ├── auth/                 # login, register
│   ├── dashboard.html        # Role-based dashboard
│   ├── patients/             # list, add, edit
│   ├── doctors/              # list, add, edit
│   ├── appointments/         # list, book, edit
│   └── billing/              # list, generate
└── static/                   # CSS & JS assets
    ├── css/style.css
    └── js/main.js
```

---

## Database Schema

| Table | Columns |
|-------|---------|
| `users` | id, name, email, password_hash, role, created_at |
| `patients` | id, user_id, name, age, gender, phone, address, created_at |
| `doctors` | id, name, specialty, phone, email, created_at |
| `appointments` | id, patient_id, doctor_id, appointment_date, appointment_time, status, notes, created_at |
| `billings` | id, appointment_id, amount, description, status, created_at |

---

## Roles & Permissions

| Action | Admin | Doctor | Patient |
|--------|:-----:|:------:|:-------:|
| Manage Doctors | Yes | No | No |
| Manage Patients | Yes | Yes | No |
| Book Appointments | Yes | Yes | No |
| Generate Invoices | Yes | No | No |
| View Dashboard | Yes | Yes | Yes |

---

## Testing

Run the application and visit the following routes:

- `GET /login` — Login page
- `GET /register` — Registration page
- `GET /` — Dashboard (requires login)
- `GET /patients` — Patient list (Admin/Doctor)
- `GET /doctors` — Doctor list (Admin)
- `GET /appointments` — Appointments (Admin/Doctor)
- `GET /billing` — Billing list (Admin)

---

## License

This project is for educational purposes as part of a capstone project.
"""

# Write files using UTF-8 encoding
(ROOT / "static" / "css" / "style.css").write_text(css, encoding="utf-8")
(ROOT / "static" / "js" / "main.js").write_text(js, encoding="utf-8")
(ROOT / "requirements.txt").write_text(requirements, encoding="utf-8")
(ROOT / "README.md").write_text(readme, encoding="utf-8")

print("Static files, requirements, and README created successfully.")