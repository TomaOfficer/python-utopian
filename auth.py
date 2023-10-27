from authlib.integrations.flask_client import OAuth

def configure_oauth(app, config):
    oauth = OAuth(app)

    oauth.register('github',
        client_id=config['github_client_id'],
        client_secret=config['github_client_secret'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )
    
    oauth.register('google',
        client_id=config['google_client_id'],
        client_secret=config['google_client_secret'],
        request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'},
        base_url='https://www.googleapis.com/oauth2/v1/',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth'
    )

    return oauth

