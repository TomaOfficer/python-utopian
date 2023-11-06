from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the function that will use the CSV agent to answer questions
def csv_agent_query_function(question, csv_path='example_data/October2023_3780.csv'):
    # Create the CSV agent
    csv_agent = create_csv_agent(
        llm=OpenAI(temperature=0), 
        path=csv_path,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    # Run the agent with the question
    return csv_agent.run(question)

# # Hardcoded question
# hardcoded_question = "How much has been spent on food related items?"

# # Get the answer to the hardcoded question
# answer = csv_agent_query_function(hardcoded_question)

# # Print the answer to the console
# print(f"Question: {hardcoded_question}")
# print(f"Answer: {answer}")
