"""Generate missing template files for the Hospital Management System."""
import pathlib

ROOT = pathlib.Path(__file__).parent / "hospital_management" / "templates"

# Billing generate page
billing_generate = """{% extends "base.html" %}

{% block title %}Generate Invoice{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Generate Invoice</h2>
    <a href="{{ url_for('billing.list') }}" class="btn btn-secondary">Back</a>
</div>

<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label for="appointment" class="form-label">Appointment</label>
                <select class="form-select" id="appointment" name="appointment_id" required>
                    {% for appointment in appointments %}
                    <option value="{{ appointment.id }}">#{{ appointment.id }} - {{ appointment.patient_name }} with {{ appointment.doctor_name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label for="amount" class="form-label">Amount</label>
                <input type="number" step="0.01" class="form-control" id="amount" name="amount" required>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" name="description" rows="2"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Generate Invoice</button>
        </form>
    </div>
</div>
{% endblock content %}
"""

# Appointment edit page (already exists? just make sure)
appointment_edit = """{% extends "base.html" %}

{% block title %}Edit Appointment{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Edit Appointment</h2>
    <a href="{{ url_for('appointment.list') }}" class="btn btn-secondary">Back</a>
</div>

<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label for="patient" class="form-label">Patient</label>
                <select class="form-select" id="patient" name="patient_id" required>
                    {% for patient in patients %}
                    <option value="{{ patient.id }}" {% if patient.id == appointment.patient_id %}selected{% endif %}>{{ patient.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label for="doctor" class="form-label">Doctor</label>
                <select class="form-select" id="doctor" name="doctor_id" required>
                    {% for doctor in doctors %}
                    <option value="{{ doctor.id }}" {% if doctor.id == appointment.doctor_id %}selected{% endif %}>{{ doctor.name }} - {{ doctor.specialty }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label for="date" class="form-label">Date</label>
                <input type="date" class="form-control" id="date" name="appointment_date" value="{{ appointment.appointment_date }}" required>
            </div>
            <div class="mb-3">
                <label for="time" class="form-label">Time</label>
                <input type="time" class="form-control" id="time" name="appointment_time" value="{{ appointment.appointment_time }}" required>
            </div>
            <div class="mb-3">
                <label for="status" class="form-label">Status</label>
                <select class="form-select" id="status" name="status" required>
                    <option value="scheduled" {% if appointment.status == 'scheduled' %}selected{% endif %}>Scheduled</option>
                    <option value="completed" {% if appointment.status == 'completed' %}selected{% endif %}>Completed</option>
                    <option value="cancelled" {% if appointment.status == 'cancelled' %}selected{% endif %}>Cancelled</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="notes" class="form-label">Notes</label>
                <textarea class="form-control" id="notes" name="notes" rows="2">{{ appointment.notes }}</textarea>
            </div>
            <button type="submit" class="btn btn-primary">Update Appointment</button>
        </form>
    </div>
</div>
{% endblock content %}
"""

# Doctor edit page
doctor_edit = """{% extends "base.html" %}

{% block title %}Edit Doctor{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Edit Doctor</h2>
    <a href="{{ url_for('doctor.list') }}" class="btn btn-secondary">Back</a>
</div>

<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="name" name="name" value="{{ doctor.name }}" required>
            </div>
            <div class="mb-3">
                <label for="specialty" class="form-label">Specialty</label>
                <input type="text" class="form-control" id="specialty" name="specialty" value="{{ doctor.specialty }}" required>
            </div>
            <div class="mb-3">
                <label for="phone" class="form-label">Phone</label>
                <input type="text" class="form-control" id="phone" name="phone" value="{{ doctor.phone }}" required>
            </div>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email" value="{{ doctor.email }}" required>
            </div>
            <button type="submit" class="btn btn-primary">Update Doctor</button>
        </form>
    </div>
</div>
{% endblock content %}
"""

# Write all files
(ROOT / "billing" / "generate.html").write_text(billing_generate)
(ROOT / "appointments" / "edit.html").write_text(appointment_edit)
(ROOT / "doctors" / "edit.html").write_text(doctor_edit)

print("Templates created successfully.")