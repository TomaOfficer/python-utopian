import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Poetic Programming Assistant",
    instructions="You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

def main():
    while True:
      thread = client.beta.threads.create()

      user_input = input("Ask your poetic assistant: ")
      if user_input.lower() == 'exit':
          print("Goodbye!")
          break

      message_response = client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=user_input
      )
      print("Message Response:", message_response)  # Debugging

      run_response = client.beta.threads.runs.create(
          thread_id=thread.id,
          assistant_id=assistant.id
      )
      print("Run Response:", run_response)  # Debugging

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
              print(message.content)

      run_steps = client.beta.threads.runs.steps.list(
          thread_id=thread.id,
          run_id=run_response.id
      )
      print("\nRun Steps:")
      for step in run_steps.data:
          print(f"Step ID: {step.id}, Type: {step.type}, Status: {step.status}")

if __name__ == "__main__":
    main()
