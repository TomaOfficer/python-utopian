from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMMathChain
# from langchain_csv_agent import csv_agent_query_function 
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0.01, model="gpt-4", max_tokens=3600)
llm_math = LLMMathChain.from_llm(llm)

tools = [
  Tool(
    name="Calculator",
    description=
    "Useful for when you need to do math or calculate expressions. Please provide an expression.",
    func=llm_math.run,
    return_direct=True),
  # Tool(
  #     name="October 2023 expenses",
  #     description="Searches for data pertaining to October 2023 expenses.",
  #     func=lambda q: csv_agent_query_function(q),  # Pass the function as a lambda to delay execution
  #     return_direct=True
  # )
]

memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools,
                               llm,
                               agent="conversational-react-description",
                               verbose=True,
                               handle_parsing_errors=True,
                               memory=memory)

# Hardcoded question for the CSV agent
hardcoded_question = "What are the top three categories of expense that you see in the data? Please just give me the category names that you come up with."

# Run the main agent chain with the hardcoded question
answer = agent_chain.run(input=hardcoded_question)

# Print the answer to the console
print(f"Question: {hardcoded_question}")
print(f"Answer: {answer}")