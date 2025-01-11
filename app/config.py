"""
Here we configure the SECRET_KEY, JWT secret, and the database URI for SQLite.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Fallback to default for local testing
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
