"""
Configuration module for the application
"""
import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DB_DIR = BASE_DIR / "db"

# Database configuration
DB_PATH = str(DB_DIR / "clinic.db")

# API configuration
API_TITLE = "Dental Clinic API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API for managing dental clinic services, doctors, customers, and appointments"

# CORS configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Environment
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
