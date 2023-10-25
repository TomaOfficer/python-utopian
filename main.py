from flask import Flask, render_template, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_if_not_found')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.String(50), unique=True)

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
        return 'Access denied: reason={} error={}'.format(
            request.args.get('error_reason', 'No reason provided'),
            request.args.get('error_description', 'No description provided')
        )
    
    session['github_token'] = (response['access_token'], '')
    github_user = github.get('user').data
    github_id = str(github_user['id'])  # Unique GitHub user ID
    
    # Check if user exists in your database
    user = User.query.filter_by(github_id=github_id).first()
    
    if user is None:
        # Create new user in your database
        new_user = User(github_id=github_id)
        db.session.add(new_user)
        db.session.commit()
    
    # Set up session or whatever you need to keep the user logged in
    session['user_id'] = github_id

    return redirect(url_for('authorized_success'))

@app.route('/authorized_success')
def authorized_success():
    return render_template('authorized.html', token=session.get('github_token')[0], user_db_id=session['user_id'])


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This line creates the tables based on your SQLAlchemy models
    app.run(debug=True)
