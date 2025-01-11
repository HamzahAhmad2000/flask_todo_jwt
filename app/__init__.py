"""
We initialize Flask, the database, the JWT manager, and register Blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .config import Config
from dotenv import load_dotenv


load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    """ Application factory to create and configure the Flask app. """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Import and register blueprints
    from .auth.routes import auth_bp
    from .tasks.routes import tasks_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    with app.app_context():
        db.create_all()

    return app
