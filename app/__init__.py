#Initializes the Flask app, blueprints, extensions

from flask import Flask
from app.utils.logging import setup_logging
from flask_pymongo import PyMongo
import logging
mongo=PyMongo()
from app.config import Config , TestConfig

def create_app(config_class=Config):
    """
        Application factory function to create and configure the Flask app for different env configuration.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_object(config_class)  # Load from your config.py

    # Initialize extensions
    mongo.init_app(app)
    setup_logging()

    # Register Blueprints
    from app.views.home import home_bp
    app.register_blueprint(home_bp)

    return app