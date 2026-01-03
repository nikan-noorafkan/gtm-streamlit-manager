import streamlit as st
import json
from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.readonly",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
]

def login():
    if "oauth_client" not in st.session_state:
        st.warning("Please provide your Google OAuth credentials first.")
        st.stop()

    oauth = st.session_state["oauth_client"]

    client_config = {
        "web": {
            "client_id": oauth["client_id"],
            "client_secret": oauth["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [oauth["redirect_uri"]],
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=oauth["redirect_uri"],
    )

    query_params = st.query_params

    if "code" not in query_params:
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        st.link_button("Login with Google", auth_url)
        st.stop()

    flow.fetch_token(code=query_params["code"])
    st.session_state["credentials"] = flow.credentials


def get_credentials():
    return st.session_state.get("credentials")
