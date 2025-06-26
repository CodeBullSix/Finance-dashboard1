
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="AI-Enhanced Financial Planner", layout="wide")
st.title("🧠 Financial + Longevity Dashboard")

# Session state for login simulation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Enter your username to continue:")
    if st.button("Login") and username:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.experimental_rerun()
    st.stop()

# Load transaction data
@st.cache_data
def load_data():
    return pd.read_csv("data/sample_transactions.csv", parse_dates=["Date"])

df = load_data()

# Metrics
income = df[df["Amount"] > 0]["Amount"].sum()
expenses = -df[df["Amount"] < 0]["Amount"].sum()
net = income - expenses

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"£{income:.2f}")
col2.metric("Total Expenses", f"£{expenses:.2f}")
col3.metric("Net Savings", f"£{net:.2f}")

# Charts
st.subheader("📊 Spending by Category")
category_summary = df[df["Amount"] < 0].groupby("Category")["Amount"].sum().reset_index()
fig1 = px.bar(category_summary, x="Category", y="Amount", title="Spending Breakdown by Category")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📅 Cumulative Cash Flow")
df["Net"] = df["Amount"]
daily = df.groupby("Date")["Net"].sum().cumsum().reset_index()
fig2 = px.line(daily, x="Date", y="Net", title="Cumulative Net Cash Flow")
st.plotly_chart(fig2, use_container_width=True)

# Investment Portfolio Section
st.subheader("📈 Investment Portfolio Tracker")
with st.form("investment_form"):
    asset = st.text_input("Asset (e.g., NVDA, ETH, VTI)")
    amount_invested = st.number_input("Amount Invested (£)", min_value=0.0)
    current_value = st.number_input("Current Value (£)", min_value=0.0)
    submitted = st.form_submit_button("Add Investment")
    if submitted and asset:
        new_row = {"Asset": asset, "Invested": amount_invested, "Current": current_value}
        if "investments" not in st.session_state:
            st.session_state.investments = []
        st.session_state.investments.append(new_row)

if "investments" in st.session_state:
    inv_df = pd.DataFrame(st.session_state.investments)
    inv_df["Gain/Loss (£)"] = inv_df["Current"] - inv_df["Invested"]
    inv_df["% Change"] = (inv_df["Gain/Loss (£)"] / inv_df["Invested"]) * 100
    st.dataframe(inv_df)

    fig3 = px.bar(inv_df, x="Asset", y="Gain/Loss (£)", color="Asset", title="Investment Performance")
    st.plotly_chart(fig3, use_container_width=True)

# Longevity Goal Tracker
st.subheader("🧬 Longevity & AI Integration Goals")
goals = {
    "AI Integration Fund (£10,000 target)": 10000,
    "Longevity Treatments (£5,000 target)": 5000,
    "Emergency Health Buffer (£2,000 target)": 2000
}

if "goal_progress" not in st.session_state:
    st.session_state.goal_progress = {k: 0 for k in goals}

for goal, target in goals.items():
    current = st.slider(f"{goal}", 0, target, st.session_state.goal_progress[goal], step=100)
    st.session_state.goal_progress[goal] = current
    progress = current / target
    st.progress(progress, text=f"£{current:,} of £{target:,}")

# Upload
st.sidebar.header("Upload Your Statement")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df_new = pd.read_csv(uploaded, parse_dates=["Date"])
    df_new.to_csv("data/sample_transactions.csv", index=False)
    st.sidebar.success("Upload complete! Refresh to apply new data.")

:
    st.session_state.logged_in = False

# Simple login simulation
if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if username == "admin" and password == "pass123":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.stop()

# Load transaction data
@st.cache_data
def load_data():
    path = "data/sample_transactions.csv"
    return pd.read_csv(path, parse_dates=["Date"])

df = load_data()

# Financial Overview
st.subheader("💰 Overview")
income = df[df["Amount"] > 0]["Amount"].sum()
expenses = -df[df["Amount"] < 0]["Amount"].sum()
net = income - expenses

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"£{income:.2f}")
col2.metric("Total Expenses", f"£{expenses:.2f}")
col3.metric("Net Savings", f"£{net:.2f}")

# Spending by Category
st.subheader("📂 Spending by Category")
category_summary = df[df["Amount"] < 0].groupby("Category")["Amount"].sum().reset_index()
fig = px.bar(category_summary, x="Category", y="Amount", title="Spending by Category", labels={"Amount": "Spent (£)"})
st.plotly_chart(fig, use_container_width=True)

# Investment Tracking
st.subheader("📈 Investment Portfolio")
investments = st.text_area("Enter your investments (Asset,Amount Invested,Current Value)", 
                           value="NVDA,500,800\nETH,200,450\nARKG,300,310")

inv_df = pd.DataFrame([x.split(",") for x in investments.split("\n")], columns=["Asset", "Invested", "Current"])
inv_df["Invested"] = inv_df["Invested"].astype(float)
inv_df["Current"] = inv_df["Current"].astype(float)
inv_df["Return"] = inv_df["Current"] - inv_df["Invested"]
inv_df["% Gain"] = (inv_df["Return"] / inv_df["Invested"]) * 100

st.dataframe(inv_df)
fig2 = px.bar(inv_df, x="Asset", y="% Gain", color="Asset", title="Investment Performance")
st.plotly_chart(fig2, use_container_width=True)

# Longevity Goal Tracker
st.subheader("🧬 Longevity Goals")
goal_data = {
    "Goal": ["Neuralink Fund", "Cryonics Backup", "Health Optimization", "AI Education Fund"],
    "Target (£)": [5000, 10000, 3000, 2000],
    "Saved (£)": [1750, 2500, 900, 600]
}
goal_df = pd.DataFrame(goal_data)
goal_df["% Complete"] = (goal_df["Saved (£)"] / goal_df["Target (£)"]) * 100

st.dataframe(goal_df)
fig3 = px.bar(goal_df, x="Goal", y="% Complete", color="Goal", title="Progress Toward Longevity Goals")
st.plotly_chart(fig3, use_container_width=True)

# Upload section
st.sidebar.header("📤 Upload Your Statement")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    user_df = pd.read_csv(uploaded, parse_dates=["Date"])
    user_df.to_csv("data/sample_transactions.csv", index=False)
    st.sidebar.success("Uploaded! Refresh app to see changes.")
