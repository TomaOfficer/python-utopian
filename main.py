from flask import Flask, render_template, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_if_not_found')

oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='843d2c55ae8ae77a0598',  
    consumer_secret='49f12611eb5507da82dd2972c263d2ac4612b9c4', 
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@app.route('/')
def index():
    return render_template('index.html')  # Change this line to use render_template


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        error_reason = request.args.get('error_reason', 'No reason provided')
        error_description = request.args.get('error_description', 'No description provided')
        return f'Access denied: reason={error_reason} error={error_description}'
    
    session['github_token'] = (response['access_token'], '')
    return redirect(url_for('authorized'))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == '__main__':
    app.run(debug=True)
