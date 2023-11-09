from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from auth import configure_oauth

# Initialize extensions but don't bind to a specific app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)

    # OAuth configuration
    oauth = configure_oauth(app)

    # Register blueprints or call init_app functions from your other modules here
    # ...

    return app, oauth