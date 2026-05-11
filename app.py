import streamlit as st 
import pandas_gpt as pg
from pandas_gpt.completers.openai import OpenAI
import pandas as pd

st.title('PANDAS_GPT INTEGRATED TYPE PROMPTS AND GENERATE RESULTS IN FORMS OF EDA , VISUALISATION AND NOT JUST INSIGHTS')

pg.completer = OpenAI(
    model="openai/gpt-4.1-nano",
    base_url="https://models.github.ai/inference",
    api_key="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"
)

url = st.text_input('Enter the github link here of the csv', placeholder='https://raw.githubusercontent.com/username/repo/main/data.csv', help='Paste the raw GitHub link to your CSV file here')


if url:
  try:
    df = pd.read_csv(url)
    st.dataframe(df.head())

    question = st.text_input('Enter the question tegarding the data frame please')
    if question:
      result = df.ask(question)
      st.write(result)
  except Exception as e:
    st.write(e, "Something went wrong!")
