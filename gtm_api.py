from googleapiclient.discovery import build

def get_service(credentials):
    return build(
        "tagmanager",
        "v2",
        credentials=credentials,
        cache_discovery=False
    )

def list_accounts(service):
    return service.accounts().list().execute()

def list_containers(service, account_id: str):
    parent = f"accounts/{account_id}"
    return service.accounts().containers().list(parent=parent).execute()

def list_workspaces(service, account_id: str, container_id: str):
    parent = f"accounts/{account_id}/containers/{container_id}"
    return service.accounts().containers().workspaces().list(parent=parent).execute()

def list_tags(service, account_id: str, container_id: str, workspace_id: str):
    parent = (
        f"accounts/{account_id}"
        f"/containers/{container_id}"
        f"/workspaces/{workspace_id}"
    )
    return service.accounts().containers().workspaces().tags().list(parent=parent).execute()

def create_custom_html_tag(
    service,
    account_id: str,
    container_id: str,
    workspace_id: str,
    name: str,
    html: str
):
    parent = (
        f"accounts/{account_id}"
        f"/containers/{container_id}"
        f"/workspaces/{workspace_id}"
    )

    body = {
        "name": name,
        "type": "html",
        "parameter": [
            {
                "type": "template",
                "key": "html",
                "value": html
            }
        ]
    }

    return (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .create(parent=parent, body=body)
        .execute()
    )

def update_custom_html_tag(
    service,
    account_id: str,
    container_id: str,
    workspace_id: str,
    tag_id: str,
    name: str,
    html: str
):
    path = (
        f"accounts/{account_id}"
        f"/containers/{container_id}"
        f"/workspaces/{workspace_id}"
        f"/tags/{tag_id}"
    )

    body = {
        "name": name,
        "type": "html",
        "parameter": [
            {
                "type": "template",
                "key": "html",
                "value": html
            }
        ]
    }

    return (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .update(
            path=path,
            body=body,
        )
        .execute()
    )

