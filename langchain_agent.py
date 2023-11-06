from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMMathChain
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4")
llm_math = LLMMathChain.from_llm(llm)

tools = [
  Tool(
    name="Calculator",
    description=
    "Useful for when you need to do math or calculate expressions. Please provide an expression.",
    func=llm_math.run,
    return_direct=True)
]

memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools,
                               llm,
                               agent="conversational-react-description",
                               memory=memory)

# Hardcoded question
hardcoded_question = "What is 5 times 150?"

# Run the agent chain with the hardcoded question
answer = agent_chain.run(input=hardcoded_question)

# Print the answer to the console
print(f"Question: {hardcoded_question}")
print(f"Answer: {answer}")