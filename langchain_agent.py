from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0)

tools = load_tools(
  ["llm-math"], 
  llm=llm
)

agent_executor = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent_executor.invoke(
    {
        "input": "What is 5 times 2?"
    }
)