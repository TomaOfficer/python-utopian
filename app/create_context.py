import os
import openai
from flask import Blueprint, request, session, redirect, url_for, jsonify

# Load environment variables and initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

context_blueprint = Blueprint('context', __name__)

@context_blueprint.route('/create_context', methods=['POST'])
def create_context():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_input = request.form['user_input']

    try:
        prompt = f"Before you can answer the following question, what context do you need to know about the user? Here is the user's question: {user_input}"
        
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to identify and output the types of context needed to answer a user's question. Context types might include 'Income', 'Dental Health', 'Medical History', etc."},
                {"role": "user", "content": prompt},
            ]
        )

        # Parsing the response to extract context requirements
        context_requirements = response['choices'][0]['message']['content']
        # Format the output as JSON (or any other desired format)
        formatted_response = {"required_context": context_requirements}

        return jsonify(formatted_response)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

   

  