from flask import Blueprint, redirect, url_for, session, render_template
from flask_login import login_user, logout_user, current_user, login_required
from authlib.integrations.flask_client import OAuth
from app.extensions import db
from app.models import User
from app.create_context import RestaurantForm

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
    
    return oauth

@auth_blueprint.record_once
def on_load(state):
    # Configure the real OAuth object here
    global oauth
    oauth = configure_oauth(state.app)

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
        login_user(new_user)
    else:
        login_user(user)

    return redirect(url_for('auth.authorized_success'))

@auth_blueprint.route('/error')
def error():
    return render_template('error.html')

@auth_blueprint.route('/authorized_success')
def authorized_success():
    return render_template('authorized.html', user_db_id=session['user_id'])

@auth_blueprint.route('/talk-to-assistant')
def talk_to_assistant():
    return render_template('talk-to-assistant.html')

@auth_blueprint.route('/create-context')
@login_required
def create_context():
    form = RestaurantForm() 
    return render_template('create-context.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    session.pop('github_token', None)  
    session.pop('google_token', None) 
    return redirect(url_for('index'))