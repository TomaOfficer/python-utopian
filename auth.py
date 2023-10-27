from authlib.integrations.flask_client import OAuth

def configure_oauth(app, config):
    oauth = OAuth(app)  # Initialize OAuth with Authlib

    oauth.register('github',
        client_id=config['github_client_id'], 
        client_secret=config['github_client_secret'],
        # ... rest of your GitHub config
    )

    oauth.register('google', 
        client_id=config['google_client_id'],  
        client_secret=config['google_client_secret'],  
        # ... rest of your Google config
    )
    
    return oauth
