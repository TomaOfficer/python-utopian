from app.extensions import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
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

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legal_name = db.Column(db.String(100), nullable=False)
    business_structure = db.Column(db.String(100), nullable=False)
    ein = db.Column(db.String(100), nullable=False)
    business_address = db.Column(db.String(100), nullable=False)
    business_nature = db.Column(db.String(100), nullable=False)
    owner_info = db.Column(db.String(500), nullable=False)
    governing_law = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(500), nullable=False)

    # Foreign key to link to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to link back to the User model
    user = db.relationship('User', backref=db.backref('restaurants', lazy=True))

class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(100), nullable=False)
    travelers = db.Column(db.String(200), nullable=False)
    preferences = db.Column(db.String(400), nullable=False)
    travel_style = db.Column(db.String(400), nullable=False)
    interests = db.Column(db.String(500), nullable=False)
    special_requirements = db.Column(db.String(300), nullable=False)

    # Foreign key to link to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to link back to the User model
    user = db.relationship('User', backref=db.backref('travel_plans', lazy=True))