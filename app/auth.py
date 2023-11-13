from flask import Blueprint, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from app.extensions import db
from app.models import User

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

    session['user_id'] = {'id': github_id, 'provider': 'github'}

    return redirect(url_for('auth.authorized_success'))
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

@auth_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Ensure user is logged in

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('path/to/upload/folder', filename)
        file.save(filepath)

        new_file = UserFile(filename=filename, filepath=filepath, user_id=session['user_id']['id'])
        db.session.add(new_file)
        db.session.commit()

        return 'File uploaded successfully'
    return 'No file'