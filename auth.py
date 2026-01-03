import streamlit as st
from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.readonly",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
]


def login():
    """
    Handles Google OAuth login flow.
    Ensures the OAuth code is used only once and
    prevents re-authentication on Streamlit reruns.
    """

    # If credentials already exist, do nothing
    if "credentials" in st.session_state:
        return

    # OAuth client must be provided by the user
    if "oauth_client" not in st.session_state:
        return

    oauth_client = st.session_state["oauth_client"]
    query_params = st.query_params

    # OAuth callback with authorization code
    if "code" in query_params:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": oauth_client["client_id"],
                    "client_secret": oauth_client["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri=oauth_client["redirect_uri"],
        )

        flow.fetch_token(code=query_params["code"])

        # Store credentials in session only
        st.session_state["credentials"] = flow.credentials

        # Remove OAuth code to prevent reuse
        st.query_params.clear()

        st.success("Google authentication successful.")
        st.rerun()

    # No credentials and no code → show login button
    else:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": oauth_client["client_id"],
                    "client_secret": oauth_client["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri=oauth_client["redirect_uri"],
        )

        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )

        st.link_button("Login with Google", auth_url)


def get_credentials():
    """
    Returns OAuth credentials from the current session.
    """
    return st.session_state.get("credentials")


def logout():
    """
    Clears the current session and logs the user out.
    """
    st.session_state.pop("credentials", None)
    st.session_state.pop("oauth_client", None)
    st.query_params.clear()
    st.rerun()
