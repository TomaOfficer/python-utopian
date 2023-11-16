import os
import openai
from flask import Blueprint, request, session, redirect, url_for, jsonify
from app.models import Restaurant, User
from app.extensions import db
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Load environment variables and initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

context_blueprint = Blueprint('context', __name__)

@context_blueprint.route('/create_context', methods=['POST'])
@login_required
def create_context():
    user_input = request.form['user_input']

    try:
        prompt = f"Before you can answer the following question, what context do you need to know about the user? Here is the user's question: {user_input}"
        
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to identify and output the types of context needed to answer a user's question. Context types might include 'Income', 'Dental Health', 'Medical History', etc."},
                {"role": "user", "content": prompt},
            ]
        )

        # Parsing the response to extract context requirements
        context_requirements = response.choices[0].message.content
        formatted_response = {"response": context_requirements}  # Define formatted_response

        return jsonify(formatted_response)

        return jsonify(formatted_response)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

class RestaurantForm(FlaskForm):
    legal_name = StringField('Legal Name', validators=[DataRequired()])
    business_structure = StringField('Business Structure', validators=[DataRequired()])
    ein = StringField('Employer Identification Number (EIN)', validators=[DataRequired()])
    business_address = StringField('Business Address', validators=[DataRequired()])
    business_nature = StringField('Nature of Business', validators=[DataRequired()])
    owner_info = StringField('Owner Information', validators=[DataRequired()])
    governing_law = StringField('Governing Law', validators=[DataRequired()])
    contact_details = StringField('Contact Details', validators=[DataRequired()])
    submit = SubmitField('Submit')

@context_blueprint.route('/create_restaurant', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(
            legal_name=form.name.data,
            business_address=form.address.data,
            business_structure=form.corporate_entity_type.data,
            user_id=current_user.id  # Assuming Flask-Login is used for user management
        )
        # Add other fields as necessary
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('context.restaurant_added_successfully')) 
    return render_template('add_restaurant.html', form=form)

@context_blueprint.route('/restaurant_added_successfully')
@login_required
def restaurant_added_successfully():
    return render_template('create-context.html')

  