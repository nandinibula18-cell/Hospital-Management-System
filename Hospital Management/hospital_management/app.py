"""
Hospital Management System - Flask application entry point.
"""

import os
from flask import Flask, redirect, url_for
from models.database import init_db, seed_data
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.patient_controller import patient_bp
from controllers.doctor_controller import doctor_bp
from controllers.appointment_controller import appointment_bp
from controllers.billing_controller import billing_bp

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")


def create_app():
    """Application factory for the hospital management system."""
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database (create tables + seed admin user)
    with app.app_context():
        init_db()
        seed_data()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(billing_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)