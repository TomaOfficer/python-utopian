from flask import Blueprint, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from extensions import db
from models import User

auth_blueprint = Blueprint('auth', __name__)

def configure_oauth(app):
    oauth = OAuth(app)

    oauth.register('github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )
    
    oauth.register('google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'},
        base_url='https://www.googleapis.com/oauth2/v1/',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth'
    )

    oauth.register('linkedin',
        client_id=app.config['LINKEDIN_CLIENT_ID'],
        client_secret=app.config['LINKEDIN_CLIENT_SECRET'],
        request_token_params={'scope': 'r_liteprofile r_emailaddress'},
        base_url='https://api.linkedin.com/v2/',
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        authorize_url='https://www.linkedin.com/oauth/v2/authorization'
    )

    return oauth

@auth_blueprint.record_once
def on_load(state):
    # Configure the real OAuth object here
    global oauth
    oauth = configure_oauth(state.app)

# Linkedin login routes
@auth_blueprint.route('/login_linkedin')
def login_linkedin():
    redirect_uri = url_for('auth/authorized_linkedin', _external=True)
    return oauth.linkedin.authorize_redirect(redirect_uri, scope='openid profile email')

@auth_blueprint.route('/login_linkedin/authorized')
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

    return redirect(url_for('auth.authorized_success'))

# Github login routes
@auth_blueprint.route('/login_github')
def login_github():
    redirect_uri = url_for('auth.authorized_github', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_blueprint.route('/login_github/authorized')
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

    return redirect(url_for('auth.authorized_success'))

# Google login routes
@auth_blueprint.route('/login_google')
def login_google():
    redirect_uri = url_for('authorized_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri) 

@auth_blueprint.route('/login_google/authorized')
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

    return redirect(url_for('auth.authorized_success'))

@auth_blueprint.route('/error')
def error():
    return render_template('error.html')

@auth_blueprint.route('/authorized_success')
def authorized_success():
    return render_template('authorized.html', user_db_id=session['user_id'])

@auth_blueprint.route('/logout')
def logout():
    session.pop('github_token', None)  
    session.pop('google_token', None) 
    return redirect(url_for('index'))