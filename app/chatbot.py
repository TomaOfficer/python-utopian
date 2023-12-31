import os
from flask import Blueprint, request, session, redirect, url_for, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

chatbot_blueprint = Blueprint('chatbot', __name__)

# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("data/thomasofficer-resume.md", "rb"),
  purpose='assistants'
)

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Career Advisor",
    instructions="""You are Ward, a career advisor and teacher. Your advice is at the expert level, but you
     always keep your language accessible to a general audience. You know how to inspire curiosity by asking interesting
     questions.
    
     You're an autoregressive language model that has been fine-tuned with instruction-tuning
     and RLHF. Since you're autoregressive, each token you produce is an opportunity to use computation, therefore you
     always spend a few sentences explaining background context, assumptions, and step-by-step thinking BEFORE you to
     answer a question.
    """,
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)

@chatbot_blueprint.route('/ask_chatbot', methods=['POST'])
def ask_chatbot():
    if 'user_id' not in session:
        return redirect(url_for('index'))  

    user_input = request.form['user_input']

    try:
        # Create a thread
        thread = client.beta.threads.create()

        # Send the user's message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Create a run
        run_response = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="""Your knowledge base may include the context you need to answer the question, but it may not. 
            If you need to ask for more context, do so now. If not, go ahead and answer the question.
            """
        )

        # Poll for run completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_response.id
            )
            if run_status.status == 'completed':
                break

        # Collect and format the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        chatbot_response = ""
        for message in messages.data:
            if message.role == "assistant":
                for content_item in message.content:
                    if content_item.type == 'text':
                        chatbot_response += content_item.text.value + "\n"

        run_steps = client.beta.threads.runs.steps.list(
          thread_id=thread.id,
          run_id=run_response.id
        )
        for step in run_steps.data:
            print(f"Step ID: {step.id}, Type: {step.type}, Status: {step.status}")

        return jsonify({'response': chatbot_response})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

   

  