"""Configuration settings for the Hospital Management System."""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "hospital.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
DEBUG = True
PORT = 5000