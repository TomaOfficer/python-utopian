import os

def load_config():
    return {
        'secret_key': os.environ.get('SECRET_KEY', 'fallback_if_not_found'),
        'sqlalchemy_database_uri': 'sqlite:///users.db',  # Adjust this if you ever plan to read this from env vars
        'github_client_id': os.environ.get('GITHUB_CLIENT_ID'),
        'github_client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
        'google_client_id': os.environ.get('GOOGLE_CLIENT_ID'),  
        'google_client_secret': os.environ.get('GOOGLE_CLIENT_SECRET') 
    }
