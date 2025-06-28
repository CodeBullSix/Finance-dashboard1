
import streamlit as st
import smtplib
from email.message import EmailMessage
from collections import defaultdict

def generate_ai_summary(accounts, transactions):
    total = sum(acc['balance']['available'] for acc in accounts)
    tx_count = len(transactions)
    return f"You have {len(accounts)} account(s) with £{total/100:.2f} total. You've made {tx_count} transactions this month. Let’s optimize your savings!"

def analyze_spending(transactions):
    categories = defaultdict(int)
    for tx in transactions:
        cat = tx.get("transaction_classification", ["Other"])[0]
        categories[cat] += abs(tx["amount"])

    output = "**Suggested Adjustments:**\n"
    for cat, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        if total > 10000:  # >£100
            output += f"- 💸 High spending in **{cat}**: £{total/100:.2f}. Consider reducing this.\n"
    output += "\n✅ Tip: Try meal prepping to cut food costs or limit subscriptions."
    return output

def send_email_report(summary):
    msg = EmailMessage()
    msg["Subject"] = "Your Weekly AI Budget Report"
    msg["From"] = st.secrets["email"]["address"]
    msg["To"] = st.secrets["email"]["address"]
    msg.set_content(summary)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(st.secrets["email"]["address"], st.secrets["email"]["app_password"])
        smtp.send_message(msg)
