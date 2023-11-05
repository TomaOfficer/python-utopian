# import pandas as pd
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
import os
from dotenv import load_dotenv

load_dotenv()

agent=create_csv_agent(
  llm=OpenAI(temperature=0), 
  path='example_data/budget-breakdown.csv',
  agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
  )
print(agent.run("How much has been spent on groceries so far?"))


# def initialize_langchain_csv_agent():
#   # Quick test with pandas to see .csv
#   df = pd.read_csv('example_data/budget-breakdown.csv')
#   df.head()
#   print(df)
