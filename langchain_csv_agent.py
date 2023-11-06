from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the function that will use the CSV agent to answer questions
def csv_agent_query_function(question, csv_path='example_data/October2023_3780.csv'):
    # Create the CSV agent
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0.01, model="gpt-4", max_tokens=3600), 
        path=csv_path,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    # Set the handle_parsing_errors attribute
    csv_agent.handle_parsing_errors = True
    # Run the agent with the question
    return csv_agent.run(question)

# # Hardcoded question
# hardcoded_question = "What are the top three categories of expense that you see in the data? Please just give me the category names that you come up with."

# # Get the answer to the hardcoded question
# answer = csv_agent_query_function(hardcoded_question)

# # Print the answer to the console
# print(f"Question: {hardcoded_question}")
# print(f"Answer: {answer}")
