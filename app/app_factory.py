from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.extensions import db
from app.models import User
from app.login_config import login_manager 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)

    # Register blueprints or call init_app functions from your other modules here
    from app.auth import auth_blueprint
    from app.chatbot import chatbot_blueprint
    from app.create_context import context_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')
    app.register_blueprint(context_blueprint, url_prefix='/context')

    return app