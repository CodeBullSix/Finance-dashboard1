import streamlit as st
import pandas as pd
from utils import generate_ai_budget_plan

st.set_page_config(page_title="AI Finance Dashboard", layout="centered")
st.title("💸 AI Finance Dashboard")
st.markdown("Upload your bank statement CSV to get started.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded Transactions")
    st.dataframe(df)

    st.subheader("🧠 AI Budget Suggestions")
    plan = generate_ai_budget_plan(df)
    st.markdown(plan)
else:
    st.info("Awaiting CSV upload.")