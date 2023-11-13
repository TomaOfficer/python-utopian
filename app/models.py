from app.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_id = db.Column(db.String(50), unique=True)
    oauth_provider = db.Column(db.String(20))
    # Relationship to UserFile
    files = db.relationship('UserFile', backref='user', lazy=True)

class UserFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    filepath = db.Column(db.String(200))  # Adjust length as needed
    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)