import json
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = [
"https://www.googleapis.com/auth/tagmanager.edit.containers"
]

def login():
    # اگر قبلاً لاگین شده، دیگه OAuth نکن
    if "credentials" in st.session_state:
        return

    flow = Flow.from_client_config(
        json.loads(st.secrets["google_oauth"]["client_config_json"]),
        scopes=SCOPES,
        redirect_uri=st.secrets["app"]["base_url"],
    )

    # اگر هنوز code نداریم → بفرست لاگین
    if "code" not in st.query_params:
        auth_url, _ = flow.authorization_url(prompt="consent")
        st.link_button("Login with Google", auth_url)
        st.stop()

    # فقط یک بار token بگیر
    flow.fetch_token(code=st.query_params["code"])
    creds = flow.credentials

    # ذخیره credentials
    st.session_state["credentials"] = creds.to_json()

    # پاک کردن code از URL (خیلی مهم)
    st.query_params.clear()

    st.success("OAuth works 🎉")

def get_credentials():
    if "credentials" not in st.session_state:
        return None

    return Credentials.from_authorized_user_info(
        json.loads(st.session_state["credentials"]),
        scopes=SCOPES,
    )

