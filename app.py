import streamlit as st
import requests
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="AI Finance Dashboard", layout="wide")

st.title("💸 AI-Powered Finance Dashboard")

# Load secrets
try:
    EMAIL_USER = st.secrets["email"]["address"]
    EMAIL_PASS = st.secrets["email"]["app_password"]
    MONZO_ACCESS_TOKEN = st.secrets["monzo"]["access_token"]
except Exception as e:
    st.error("Secrets not configured properly. Please set them in Streamlit settings.")
    st.stop()

# Fetch Monzo data
def get_monzo_transactions():
    url = "https://api.monzo.com/accounts"
    headers = {"Authorization": f"Bearer {MONZO_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if "accounts" not in data or len(data["accounts"]) == 0:
        st.warning("No Monzo accounts found.")
        return pd.DataFrame()
    account_id = data["accounts"][0]["id"]

    txn_url = f"https://api.monzo.com/transactions?account_id={account_id}&expand[]=merchant"
    txn_response = requests.get(txn_url, headers=headers)
    txns = txn_response.json().get("transactions", [])
    df = pd.json_normalize(txns)
    return df

df = get_monzo_transactions()

if df.empty:
    st.warning("No transactions to display.")
else:
    df["created"] = pd.to_datetime(df["created"])
    df["amount"] = df["amount"] / 100
    df = df[["created", "description", "amount", "category"]]
    st.dataframe(df)

    st.subheader("📊 Weekly Spending Summary")
    week_df = df[df["created"] > (datetime.datetime.now() - datetime.timedelta(days=7))]
    st.bar_chart(week_df.groupby("category")["amount"].sum())

    # Email report option
    if st.button("📧 Email Me a Weekly Summary"):
        msg = EmailMessage()
        msg["Subject"] = "Your Weekly Monzo Spending Summary"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_USER
        summary = week_df.groupby("category")["amount"].sum().to_string()
        msg.set_content(f"""Here is your weekly spending summary:

{summary}""")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        st.success("Email sent!")