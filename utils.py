import openai
import streamlit as st

def generate_ai_budget_plan(df):
openai.api_key = st.secrets["openai"]["api_key"]
    sample_data = df.head(10).to_csv(index=False)
    prompt = f"""You are a personal finance expert. Based on the following bank transactions, provide budget improvement suggestions, highlight areas to cut costs, and suggest saving/investment strategies. 

CSV:
{sample_data}

Advice:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
