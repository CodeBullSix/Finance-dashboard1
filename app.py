import streamlit as st
import requests
import json
from utils import generate_ai_budget_plan

st.set_page_config(page_title="AI Finance Dashboard", layout="wide")
st.title("💼 AI Finance Dashboard with TrueLayer")

# TrueLayer login URL
auth_url = f"https://auth.truelayer.com/?" \
           f"response_type=code&client_id={st.secrets['truelayer']['CLIENT_ID']}" \
           f"&redirect_uri={st.secrets['truelayer']['REDIRECT_URI']}" \
           f"&scope=info%20accounts%20balance%20transactions&state=secure123&nonce=random"

if "access_token" not in st.session_state:
    st.markdown(f"[🔐 Connect your bank via TrueLayer]({auth_url})")
else:
    st.success("Bank connected successfully.")
    st.write("Fetching transactions and balances...")

    # Example AI feature — budget suggestions
    ai_summary = generate_ai_budget_plan(st.session_state.get("transactions", []))
    st.subheader("💡 AI-Powered Budget Insights")
    st.write(ai_summary)