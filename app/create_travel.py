import os
import openai
from flask import Blueprint, request, session, redirect, url_for, jsonify, render_template
from app.models import TravelPlan, User
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from app.extensions import db
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Load environment variables and initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

travel_blueprint = Blueprint('travel', __name__)

class TravelForm(FlaskForm):
    destination = StringField('Destination', validators=[DataRequired()])
    season = StringField('Season', validators=[DataRequired()])
    travelers = StringField('Travelers', validators=[DataRequired()])
    preferences = StringField('Travel Preferences', validators=[DataRequired()])
    travel_style = StringField('Travel Style', validators=[DataRequired()])
    interests = StringField('Interests', validators=[DataRequired()])
    special_requirements = StringField('Special Requirements', validators=[DataRequired()])
    submit = SubmitField('Submit')

@travel_blueprint.route('/add_travel', methods=['GET', 'POST'])
@login_required
def add_travel():
    form = TravelForm()
    if form.validate_on_submit():
        new_travel_plan = TravelPlan(  # Rename the variable
            destination=form.destination.data,
            season=form.season.data,
            travelers=form.travelers.data,
            preferences=form.preferences.data,
            travel_style=form.travel_style.data,
            interests=form.interests.data,
            special_requirements=form.special_requirements.data,
            user_id=current_user.id
        )
        db.session.add(new_travel_plan)
        db.session.commit()
        success_message = "Travel plan added successfully!"
    
    return render_template('travel.html', form=form, message=success_message)