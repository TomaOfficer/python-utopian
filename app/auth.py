from flask import Blueprint, redirect, url_for, session, render_template, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.login_config import login_manager
from authlib.integrations.flask_client import OAuth
from app.extensions import db
from app.models import User, Restaurant
from app.create_context import RestaurantForm
from app.app_factory import login_manager 
import jwt
import requests
import secrets
import logging

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

    oauth.register('linkedin',
        client_id=app.config['LINKEDIN_CLIENT_ID'],
        client_secret=app.config['LINKEDIN_CLIENT_SECRET'],
        base_url='https://api.linkedin.com/v2/',
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        userinfo_endpoint='https://api.linkedin.com/v2/userinfo', 
        request_token_params={'scope': 'profile email'},
        jwks_uri='https://www.linkedin.com/oauth/openid/jwks'
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
    nonce = secrets.token_urlsafe(16)
    session['linkedin_nonce'] = nonce
    print ("Nonce:", nonce)  # Debugging print

    redirect_uri = url_for('auth.authorized_linkedin', _external=True)
    response = oauth.linkedin.authorize_redirect(redirect_uri, scope='openid profile email', nonce=nonce)

    print("Authorization URL:", response.headers['Location'])

    return response

@auth_blueprint.route('/login_linkedin/authorized')
def authorized_linkedin():
    try:
        # Explicitly retrieve the client_secret
        client_secret = current_app.config.get('LINKEDIN_CLIENT_SECRET')
        print("Authorizing LinkedIn, client secret:", client_secret)

        # Explicitly include the client_secret in the token exchange
        token = oauth.linkedin.authorize_access_token(client_secret=client_secret)
        if not token:
            print("No token received")  
            return redirect(url_for('auth.error'))

        # Extract the raw ID Token from the token response
        raw_id_token = token.get('id_token')
        if not raw_id_token:
            print("No ID Token received")
            return redirect(url_for('auth.error'))

        # Print the raw ID Token for inspection
        print("Raw ID Token:", raw_id_token)

        # Get unverified claims from the ID token
        unverified_claims = jwt.get_unverified_claims(id_token)
        print("Nonce in session:", session.get('linkedin_nonce'))
        print("Unverified nonce from ID Token:", unverified_claims.get('nonce'))

        # Fetch JWKS from LinkedIn's JWKS URI
        jwks_uri = "https://www.linkedin.com/oauth/openid/jwks"
        jwks_response = requests.get(jwks_uri)
        jwks = jwks_response.json()

        # Prepare for JWKS and token decoding
        public_keys = {}
        for jwk in jwks.get('keys', []):
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

        kid = jwt.get_unverified_header(id_token)['kid']
        key = public_keys[kid]

        # Decode the ID Token using JWKS for signature verification
        decoded = jwt.decode(id_token, key, algorithms=["RS256"], audience=current_app.config.get('LINKEDIN_CLIENT_ID'))

        linkedin_id = str(decoded['sub'])  # 'sub' is the subject (user ID)

        # Check the nonce in the ID Token
        nonce_in_session = session.pop('linkedin_nonce', None)
        decoded_nonce = decoded.get('nonce')
        if not nonce_in_session or nonce_in_session != decoded_nonce:
            print("Invalid nonce")
            return redirect(url_for('auth.error'))

        user = User.query.filter_by(oauth_id=linkedin_id, oauth_provider='linkedin').first()
        if user is None:
            user = User(oauth_id=linkedin_id, oauth_provider='linkedin')
            db.session.add(user)
            db.session.commit()

        login_user(user)
        session['user_id'] = user.id

        return redirect(url_for('auth.authorized_success'))

    except Exception as e:
        print("Exception in LinkedIn OAuth:", e) 
        return redirect(url_for('auth.error'))
    
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
        user = User(oauth_id=github_id, oauth_provider='github')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    session['user_id'] = user.id  # Set the session variable here

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
    restaurants = Restaurant.query.filter_by(user_id=current_user.id).all()  # Fetch restaurants for the current user
    return render_template('create-context.html', form=form, restaurants=restaurants)

@auth_blueprint.route('/travel')
@login_required
def travel():
    logging.info(f"Current User: {current_user}, Authenticated: {current_user.is_authenticated}")
    logging.info(f"Session: {session}")
    return render_template('travel.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('github_token', None)  
    session.pop('google_token', None) 
    return redirect(url_for('index'))