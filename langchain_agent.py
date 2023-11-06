from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMMathChain
from llama_index_rag import llama_index_answer_question
# from langchain_csv_agent import csv_agent_query_function 
from dotenv import load_dotenv
import os

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
  Tool(
      name="Trying Not to Try",
      description="A book about Wu-wei.",
      func=lambda q: llama_index_answer_question(q),  # Pass the function as a lambda to delay execution
      return_direct=True
  )
]

# Conversational agent memory
memory = ConversationBufferMemory(
  memory_key="chat_history",
  k=3,
  return_messages=True
  )

# Create agent
agent_chain = initialize_agent(tools,
                               llm,
                               agent="chat-conversational-react-description",
                               verbose=True,
                               handle_parsing_errors=True,
                               max_iterations=3,
                               memory=memory)

# Hardcoded question for the CSV agent
hardcoded_question = ""

# Run the main agent chain with the hardcoded question
answer = agent_chain.run(input=hardcoded_question)

# Print the answer to the console
print(f"Question: {hardcoded_question}")
print(f"Answer: {answer}")