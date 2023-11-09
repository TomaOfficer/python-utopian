from authlib.integrations.flask_client import OAuth

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

