from mock_jira import get_mock_tickets

USE_REAL_JIRA = False

JIRA_BASE_URL = ""
JIRA_EMAIL = ""
JIRA_API_TOKEN = ""
JIRA_PROJECT_KEY = ""

def get_tickets():
    if USE_REAL_JIRA:
        return get_real_jira_tickets()
    else:
        return get_mock_tickets()

def get_real_jira_tickets():
    import requests
    from requests.auth import HTTPBasicAuth
    import json

    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    jql = f'project = "{JIRA_PROJECT_KEY}" AND sprint in openSprints()'
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    params = {"jql": jql, "maxResults": 50}

    response = requests.get(url, headers=headers, auth=auth, params=params)
    issues = response.json().get("issues", [])

    tickets = []
    for issue in issues:
        fields = issue["fields"]
        tickets.append({
            "id": issue["key"],
            "summary": fields.get("summary", ""),
            "description": str(fields.get("description") or ""),
            "status": fields["status"]["name"],
            "priority": fields["priority"]["name"],
            "assignee": fields["assignee"]["displayName"]
                if fields.get("assignee") else "Unassigned",
            "story_points": fields.get("story_points", 0)
        })

    return {
        "project": JIRA_PROJECT_KEY,
        "sprint": "Current sprint",
        "total_tickets": len(tickets),
        "tickets": tickets
    }