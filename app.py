
import streamlit as st
import webbrowser
from truelayer_auth import get_auth_url, exchange_code_for_token, get_account_data, get_transactions
from utils import send_email_report, generate_ai_summary, analyze_spending

st.set_page_config(page_title="AI Finance Dashboard", layout="wide")
st.title("🤖 AI Finance Dashboard with TrueLayer & Smart Budgeting")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if st.session_state["access_token"] is None:
    st.subheader("🔐 Connect your bank to begin")
    if st.button("🔗 Connect via TrueLayer"):
        auth_url = get_auth_url()
        st.markdown(f"[Open Login Page]({auth_url})")

    code = st.text_input("Paste the code from redirect URL here (after ?code=)", "")
    if st.button("Submit Code") and code:
        token_data = exchange_code_for_token(code)
        if token_data:
            st.session_state["access_token"] = token_data["access_token"]
            st.success("✅ Connected successfully!")
        else:
            st.error("❌ Failed to authenticate.")
else:
    st.success("✅ Bank Connected")

    accounts = get_account_data(st.session_state["access_token"])
    transactions = get_transactions(st.session_state["access_token"])

    if accounts:
        st.subheader("🏦 Bank Accounts")
        for acc in accounts:
            st.write(f"**{acc['name']}** — £{acc['balance']['available']/100:.2f}")

        st.subheader("📊 AI Budget Summary")
        summary = generate_ai_summary(accounts, transactions)
        st.write(summary)

        st.subheader("💡 AI Spending Insights")
        suggestions = analyze_spending(transactions)
        st.write(suggestions)

        if st.button("📤 Email Me This Report"):
            send_email_report(summary + "\n\n" + suggestions)
            st.success("Sent to your inbox!")
    else:
        st.warning("⚠️ No accounts returned.")
