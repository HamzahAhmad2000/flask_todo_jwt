"""
Blueprint for user authentication (register and login).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask import current_app
import re

from .. import db, bcrypt
from ..models import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Requires JSON with 'username' and 'password'.
    Enforces password complexity:
      - At least 8 characters
      - At least one uppercase letter
      - At least one lowercase letter
      - At least one digit
      - At least one special character
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    # Validate username
    if not username or len(username.strip()) == 0:
        return jsonify({"message": "Username is required"}), 400

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    # Validate password complexity
    if not is_valid_password(password):
        return jsonify({
            "message": (
                "Password must be at least 8 characters and include uppercase, "
                "lowercase, digit, and special character."
            )
        }), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create and save new user
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login a user. 
    Requires JSON with 'username' and 'password'.
    Returns a JWT access token upon successful authentication.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401

    # Verify password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Create a JWT access token
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


def is_valid_password(password):
    """
    Validate password complexity.
    - At least 8 characters
    - Contains uppercase, lowercase, digit, and special character
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True
