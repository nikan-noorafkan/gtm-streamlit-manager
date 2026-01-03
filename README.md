# GTM API Manager (Streamlit)

A simple, secure UI for managing Google Tag Manager using the official GTM API.

## Features
- Google OAuth login (per-user, no shared access)
- List Accounts / Containers / Workspaces
- List Tags
- Create Custom HTML Tags
- Update existing Custom HTML Tags
- Workspace-safe (no auto-publish)

## How it works
- Each user logs in with their own Google account
- Permissions are enforced by GTM & OAuth scopes
- No data is stored server-side

## Local setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

