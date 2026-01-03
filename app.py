import streamlit as st
from auth import login, get_credentials
from gtm_api import get_service, list_accounts, list_containers, list_workspaces

st.title("GTM API Manager")

redirect_uri = st.secrets["app"]["base_url"]

with st.expander("🔐 Google OAuth Setup (Required)", expanded=True):
    client_id = st.text_input("Google OAuth Client ID")
    client_secret = st.text_input(
        "Google OAuth Client Secret",
        type="password"
    )

    st.caption("Use this redirect URI in your Google OAuth client:")
    st.code(redirect_uri, language="text")

    if st.button("Save OAuth Credentials"):
        if not client_id or not client_secret:
            st.error("Both Client ID and Client Secret are required.")
            st.stop()

        st.session_state["oauth_client"] = {
            "client_id": client_id.strip(),
            "client_secret": client_secret.strip(),
            "redirect_uri": redirect_uri,
        }

        st.success("OAuth credentials saved. Please login with Google.")

login()
credentials = get_credentials()
if not credentials:
    st.stop()

service = get_service(credentials)

# ---------- Accounts ----------
accounts = list_accounts(service).get("account", [])
accounts = sorted(accounts, key=lambda a: (a.get("name", ""), a.get("accountId", "")))

account_by_id = {a["accountId"]: a for a in accounts}
account_ids = [a["accountId"] for a in accounts]

st.subheader("Account")
selected_account_id = st.selectbox(
    "Select account",
    options=account_ids,
    format_func=lambda aid: f"{account_by_id[aid]['name']} ({aid})",
    key="account_id_select"
)

# ---------- Containers ----------
containers = list_containers(service, selected_account_id).get("container", [])
containers = sorted(containers, key=lambda c: (c.get("name", ""), c.get("containerId", "")))

container_by_id = {c["containerId"]: c for c in containers}
container_ids = [c["containerId"] for c in containers]

st.subheader("Container")
selected_container_id = st.selectbox(
    "Select container",
    options=container_ids,
    format_func=lambda cid: f"{container_by_id[cid]['name']} ({cid})",
    key=f"container_id_select_{selected_account_id}"
)

# ---------- Workspaces ----------
workspaces = list_workspaces(
    service,
    selected_account_id,
    selected_container_id
).get("workspace", [])

if not workspaces:
    st.warning("No workspaces found.")
    st.stop()

workspaces = sorted(workspaces, key=lambda w: (w.get("name", ""), w.get("workspaceId", "")))

workspace_by_id = {w["workspaceId"]: w for w in workspaces}
workspace_ids = [w["workspaceId"] for w in workspaces]

st.subheader("Workspace")
selected_workspace_id = st.selectbox(
    "Select workspace",
    options=workspace_ids,
    format_func=lambda wid: f"{workspace_by_id[wid]['name']} ({wid})",
    key=f"workspace_id_select_{selected_container_id}"
)

st.success(
    f"""
Selected:
- Account: {account_by_id[selected_account_id]['name']}
- Container: {container_by_id[selected_container_id]['name']}
- Workspace: {workspace_by_id[selected_workspace_id]['name']}
"""
)

from gtm_api import list_tags

st.subheader("Tags in Workspace")

tags_response = list_tags(
    service,
    selected_account_id,
    selected_container_id,
    selected_workspace_id
)

tags = tags_response.get("tag", [])

if not tags:
    st.info("No tags found in this workspace.")
else:
    for tag in sorted(tags, key=lambda t: t.get("name", "")):
        st.markdown(
            f"""
**{tag['name']}**
- Type: `{tag.get('type')}`
- Tag ID: `{tag.get('tagId')}`
---
"""
        )

from gtm_api import create_custom_html_tag

st.divider()
st.subheader("Create Custom HTML Tag")

with st.form("create_tag_form"):
    tag_name = st.text_input("Tag name")
    tag_html = st.text_area("HTML code", height=200)
    submit = st.form_submit_button("Create Tag")

if submit:
    if not tag_name or not tag_html:
        st.error("Tag name and HTML are required.")
    else:
        try:
            result = create_custom_html_tag(
                service,
                selected_account_id,
                selected_container_id,
                selected_workspace_id,
                tag_name,
                tag_html,
            )
            st.success(f"Tag created: {result['name']}")
        except Exception as e:
            st.error(str(e))

st.divider()
st.subheader("Edit Custom HTML Tag")

# فقط HTML tags
html_tags = [
    t for t in tags
    if t.get("type") == "html"
]

if not html_tags:
    st.info("No Custom HTML tags found in this workspace.")
else:
    tag_by_id = {t["tagId"]: t for t in html_tags}
    tag_ids = [t["tagId"] for t in html_tags]

    selected_tag_id = st.selectbox(
        "Select tag to edit",
        options=tag_ids,
        format_func=lambda tid: f"{tag_by_id[tid]['name']} ({tid})",
        key=f"edit_tag_select_{selected_workspace_id}"
    )

    selected_tag = tag_by_id[selected_tag_id]

    # پیدا کردن HTML فعلی
    html_param = next(
        (
            p["value"]
            for p in selected_tag.get("parameter", [])
            if p.get("key") == "html"
        ),
        ""
    )

    with st.form("update_tag_form"):
        new_name = st.text_input(
            "Tag name",
            value=selected_tag["name"]
        )
        new_html = st.text_area(
            "HTML code",
            value=html_param,
            height=200
        )
        update_submit = st.form_submit_button("Update Tag")

    if update_submit:
        try:
            result = update_custom_html_tag(
                service,
                selected_account_id,
                selected_container_id,
                selected_workspace_id,
                selected_tag_id,
                new_name,
                new_html,
            )
            st.success(f"Tag updated: {result['name']}")
        except Exception as e:
            st.error(str(e))

