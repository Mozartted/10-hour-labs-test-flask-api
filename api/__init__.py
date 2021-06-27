"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
# from ddtrace import patch_all
from flask_migrate import Migrate

# db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)
# patch_all()

migrate = Migrate(app, db)
def create_app():
    """Construct the core application."""
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app
