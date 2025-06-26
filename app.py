
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import smtplib
from PyPDF2 import PdfReader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re

st.set_page_config(page_title="Finance AI Dashboard", layout="wide")
st.title("💸 AI-Powered Finance Dashboard")

# Load secrets
MONZO_ACCESS_TOKEN = st.secrets["monzo"]["access_token"]
EMAIL_USER = st.secrets["email"]["address"]
EMAIL_PASS = st.secrets["email"]["app_password"]
EMAIL_TO = EMAIL_USER

# Load Monzo transactions
def get_monzo_transactions():
    acc_resp = requests.get(
        "https://api.monzo.com/accounts",
        headers={"Authorization": f"Bearer {MONZO_ACCESS_TOKEN}"}
    )
    acc_id = acc_resp.json()["accounts"][0]["id"]
    txn_resp = requests.get(
        f"https://api.monzo.com/transactions?account_id={acc_id}&expand[]=merchant",
        headers={"Authorization": f"Bearer {MONZO_ACCESS_TOKEN}"}
    )
    transactions = txn_resp.json().get("transactions", [])
    records = []
    for txn in transactions:
        if not txn.get("decline_reason") and txn["amount"] < 0:
            date = txn["created"][:10]
            desc = txn.get("merchant", {}).get("name") or txn.get("description")
            amt = abs(txn["amount"]) / 100
            records.append((date, desc, amt))
    return pd.DataFrame(records, columns=["Date", "Description", "Amount"])

# Categorize transactions
def categorize(desc):
    categories = {
        "groceries": ["Tesco", "Sainsbury", "Asda", "Lidl", "Aldi"],
        "transport": ["Shell", "Esso", "BP", "Train", "Uber"],
        "subscriptions": ["Spotify", "Netflix", "Apple", "Amazon", "H3G"],
        "insurance": ["Insurance", "Direct Line", "Admiral"],
        "food_out": ["KFC", "McDonalds", "JustEat", "Deliveroo", "Burger"],
        "other": []
    }
    for cat, keys in categories.items():
        if any(k.lower() in desc.lower() for k in keys):
            return cat
    return "other"

# Send email
def send_email(body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = "Your Weekly Budget Report"
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

# Dashboard logic
try:
    df = get_monzo_transactions()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Category"] = df["Description"].apply(categorize)

    st.subheader("🧾 Transaction History")
    st.dataframe(df)

    st.subheader("📊 Weekly Spending Overview")
    weekly = df.groupby("Week")["Amount"].sum().reset_index()
    fig = px.bar(weekly, x="Week", y="Amount", title="Spending per Week (£)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📂 Category Breakdown")
    cat_sum = df.groupby("Category")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
    st.dataframe(cat_sum)
    pie = px.pie(cat_sum, values="Amount", names="Category", title="Spending by Category")
    st.plotly_chart(pie, use_container_width=True)

    st.subheader("💡 AI Budget Suggestion")
    top = cat_sum.iloc[0]
    tip = f"Your biggest spend is on **{top['Category']}** (£{top['Amount']:.2f}). "
    if top['Category'] == "food_out":
        tip += "Cut back on takeaways and prep meals."
    elif top['Category'] == "subscriptions":
        tip += "Pause unused services to save."
    elif top['Category'] == "transport":
        tip += "Try carpooling or smarter routes."
    else:
        tip += "Keep tracking this closely."
    st.markdown(tip)

    st.subheader("📧 Send Budget Report")
    if st.button("Email Me This Week's Report"):
        email_body = f"Weekly Spend: £{weekly['Amount'].iloc[-1]:.2f}\nTop Category: {top['Category']} (£{top['Amount']:.2f})\nTip: {tip}"
        send_email(email_body)
        st.success("Email sent!")

except Exception as e:
    st.error(f"Something went wrong: {e}")
