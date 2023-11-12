from flask import Flask
from config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Register blueprints or call init_app functions from your other modules here
    from app.auth import auth_blueprint
    from app.chatbot import chatbot_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')

    return app
