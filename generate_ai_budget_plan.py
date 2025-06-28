# AI-based budget generation logic
import openai
import streamlit as st

def generate_ai_budget_plan(df):
    openai.api_key = st.secrets["openai"]["api_key"]

    summary = df[['Date', 'Amount', 'Description']].to_string(index=False)

    prompt = f"""
You are a financial assistant. Based on the transactions below, create a weekly budget plan with:
1. Expense categories that can be reduced.
2. Suggested weekly savings amount.
3. Daily habit changes to cut spending.
4. Smart tips for saving money.

Transactions:
{summary}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a budgeting expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"]
