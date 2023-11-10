import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def main():
    while True:
        # Get user input
        user_input = input("Ask your poetic assistant: ")

        # Check if the user wants to exit
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Create the completion request
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": user_input}
            ]
        )

        # Print the response
        print(completion.choices[0].message.content)

if __name__ == "__main__":
    main()