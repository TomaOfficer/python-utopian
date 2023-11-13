import os
import dotenv
from flask import render_template
from app.app_factory import create_app, db
from app.auth import auth_blueprint

# Initialization of dotenv and configuration
dotenv.load_dotenv()

app = create_app()  # This function should do all the necessary setup

# Main route
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(403)
def page_forbidden(e):
    # You can render a custom template or return a message
    return render_template('403.html'), 403

if __name__ == '__main__':
    with app.app_context():
        # Create tables and perform any initialization that requires app context
        db.create_all()

    # Start the Flask app
    app.run(debug=True)