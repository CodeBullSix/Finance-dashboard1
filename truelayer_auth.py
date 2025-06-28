import requests
import streamlit as st

def get_auth_url():
    return f"""https://auth.truelayer-sandbox.com/?response_type=code&client_id={st.secrets['truelayer']['CLIENT_ID']}&redirect_uri={st.secrets['truelayer']['REDIRECT_URI']}&scope=info%20accounts%20balance%20transactions&state=secure123&nonce=random"""

def exchange_code_for_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": st.secrets["truelayer"]["CLIENT_ID"],
        "client_secret": st.secrets["truelayer"]["CLIENT_SECRET"],
        "redirect_uri": st.secrets["truelayer"]["REDIRECT_URI"],
        "code": code,
    }
    response = requests.post("https://auth.truelayer-sandbox.com/connect/token", data=data)
    return response.json() if response.ok else None

def get_account_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.truelayer-sandbox.com/data/v1/accounts", headers=headers)
    return resp.json().get("results", []) if resp.ok else None

def get_transactions(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.truelayer-sandbox.com/data/v1/transactions"
    resp = requests.get(url, headers=headers)
    return resp.json().get("results", []) if resp.ok else []
