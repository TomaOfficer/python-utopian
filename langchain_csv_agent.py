import pandas as pd

def initialize_langchain_csv_agent():
  df = pd.read_csv('example_data/budget-breakdown.csv')
  df.head()
  print(df)