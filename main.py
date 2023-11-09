import os
import dotenv
from flask import render_template, redirect, url_for, session
from app_factory import create_app, db
from models import User

# Initialization of dotenv and configuration
dotenv.load_dotenv()

app, oauth = create_app()

# Routes
@app.route('/')
def index():
    return render_template('index.html') 

# Linkedin login routes
@app.route('/login_linkedin')
def login_linkedin():
    redirect_uri = url_for('authorized_linkedin', _external=True)
    return oauth.linkedin.authorize_redirect(redirect_uri, scope='openid profile email')

@app.route('/login_linkedin/authorized')
def authorized_linkedin():
    token = oauth.linkedin.authorize_access_token()
    if not token:
        return redirect(url_for('error'))
    resp = oauth.linkedin.get('me')
    profile = resp.json()
    linkedin_id = str(profile['id'])

    user = User.query.filter_by(oauth_id=linkedin_id, oauth_provider='linkedin').first()

    if user is None:
        new_user = User(oauth_id=linkedin_id, oauth_provider='linkedin')
        db.session.add(new_user)
        db.session.commit()

    session['user_id'] = {'id': linkedin_id, 'provider': 'linkedin'}

    return redirect(url_for('authorized_success'))

# Github login routes
@app.route('/login_github')
def login_github():
    redirect_uri = url_for('authorized_github', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@app.route('/login_github/authorized')
def authorized_github():
    token = oauth.github.authorize_access_token()
    if not token:
        return redirect(url_for('error'))
    resp = oauth.github.get('https://api.github.com/user')
    profile = resp.json()
    github_id = str(profile['id'])

    user = User.query.filter_by(oauth_id=github_id, oauth_provider='github').first()

    if user is None:
        new_user = User(oauth_id=github_id, oauth_provider='github')
        db.session.add(new_user)
        db.session.commit()

    session['user_id'] = {'id': github_id, 'provider': 'github'}

    return redirect(url_for('authorized_success'))

# Google login routes
@app.route('/login_google')
def login_google():
    redirect_uri = url_for('authorized_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri) 

@app.route('/login_google/authorized')
def authorized_google():
    token = oauth.google.authorize_access_token()
    if not token:
        return redirect(url_for('error'))
    resp = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    profile = resp.json()
    google_id = str(profile['id'])

    user = User.query.filter_by(oauth_id=google_id, oauth_provider='google').first()

    if user is None:
        new_user = User(oauth_id=google_id, oauth_provider='google')
        db.session.add(new_user)
        db.session.commit()

    session['user_id'] = google_id

    return redirect(url_for('authorized_success'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/authorized_success')
def authorized_success():
    return render_template('authorized.html', user_db_id=session['user_id'])

@app.route('/logout')
def logout():
    session.pop('github_token', None)  
    session.pop('google_token', None) 
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        # Create tables and perform any initialization that requires app context
        db.create_all()

    # Start the Flask app
    app.run(debug=True)
