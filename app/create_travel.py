import os
import openai
import logging
from flask import Blueprint, request, session, redirect, url_for, jsonify, render_template, current_app
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
    # Check if the user already has a travel plan
    existing_plan = TravelPlan.query.filter_by(user_id=current_user.id).first()

    if existing_plan:
        logging.info(f"Existing Travel Plan: Destination - {existing_plan.destination}, Season - {existing_plan.season}, Travelers - {existing_plan.travelers}, etc.")
        form = TravelForm(obj=existing_plan)
    else:
        logging.info("No existing travel plan found for this user.")
        form = TravelForm()

    # If a plan exists, prepopulate the form
    if existing_plan:
        form = TravelForm(obj=existing_plan)
    else:
        form = TravelForm()

    if form.validate_on_submit():
        if existing_plan:
            # Update existing plan
            existing_plan.destination = form.destination.data
            existing_plan.season = form.season.data
            existing_plan.travelers = form.travelers.data
            existing_plan.preferences = form.preferences.data
            existing_plan.travel_style = form.travel_style.data
            existing_plan.interests = form.interests.data
            existing_plan.special_requirements = form.special_requirements.data
            success_message = "Travel plan updated successfully!"
        else:
            # Create new plan
            new_travel_plan = TravelPlan(
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
            success_message = "Travel plan added successfully!"

        db.session.commit()

    return render_template('travel.html', form=form, message=success_message)

@travel_blueprint.route('/create_itinerary', methods=['POST'])
@login_required
def create_itinerary():
    try:
        # Retrieve the user's travel plan
        travel_plan = TravelPlan.query.filter_by(user_id=current_user.id).first()

        # Build the prompt
        prompt = f"I'm planning a trip to {travel_plan.destination} in {travel_plan.season} with {travel_plan.travelers} people. " \
                 f"I'm looking for a {travel_plan.preferences} trip, and my travel style is {travel_plan.travel_style}. " \
                 f"I'm interested in {travel_plan.interests}. " \
                 f"I have the following special requirements: {travel_plan.special_requirements}. " \
                 f"Can you help me plan my itinerary?"

        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0.1,
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant providing travel advice."},
                {"role": "user", "content": prompt},
            ]
        )

        # Parsing the response to extract context requirements
        chat_response = response.choices[0].message.content if response.choices else "No response received."
        return jsonify({'response': chat_response})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500