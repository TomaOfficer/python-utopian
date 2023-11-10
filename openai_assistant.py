import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("data/tntt.md", "rb"),
  purpose='assistants'
)

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Poetic Programming Assistant",
    instructions="You are a helpful chatbot. Use your knowledge base to best respond to customer queries.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)

def main():
    while True:
      thread = client.beta.threads.create()

      user_input = input("Ask your poetic assistant: ")
      if user_input.lower() == 'exit':
          print("Goodbye!")
          break

      message = client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=user_input
      )

      run_response = client.beta.threads.runs.create(
          thread_id=thread.id,
          assistant_id=assistant.id,
          instructions="Please address the user as Jane Doe. The user has a premium account."
      )

      # Polling for run completion
      while True:
          run_status = client.beta.threads.runs.retrieve(
              thread_id=thread.id,
              run_id=run_response.id
          )
          if run_status.status == 'completed':
              break

      messages = client.beta.threads.messages.list(thread_id=thread.id)
      for message in messages.data:
          if message.role == "assistant":
              for content_item in message.content:
                if content_item.type == 'text':
                    print(content_item.text.value)

      run_steps = client.beta.threads.runs.steps.list(
          thread_id=thread.id,
          run_id=run_response.id
      )
      for step in run_steps.data:
          print(f"Step ID: {step.id}, Type: {step.type}, Status: {step.status}")

if __name__ == "__main__":
    main()
