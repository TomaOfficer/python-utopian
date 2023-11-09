from app_factory import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_id = db.Column(db.String(50), unique=True)
    oauth_provider = db.Column(db.String(20))