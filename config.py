import os

def load_config():
    return {
        'secret_key': os.environ.get('SECRET_KEY', 'fallback_if_not_found'),
        'sqlalchemy_database_uri': 'sqlite:////Users/thomasofficer/Development/python-utopian/instance/users.db',
        'github_client_id': os.environ.get('GITHUB_CLIENT_ID'),
        'github_client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
        'google_client_id': os.environ.get('GOOGLE_CLIENT_ID'),  
        'google_client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'linkedin_client_id': os.environ.get('LINKEDIN_CLIENT_ID'),
        'linkedin_client_secret': os.environ.get('LINKEDIN_CLIENT_SECRET'),
    }
