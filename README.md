# AI Project Status Dashboard

An intelligent web app that analyzes project health and sprint status —
built to demonstrate AI-assisted program management skills.

**Live demo:** https://ai-project-dashboard-6os8.onrender.com

---

## What it does

### Manual analysis
Paste any project status update and instantly get:
- Plain-English summary of project health
- Risks flagged by severity (High / Medium / Low)
- Recommended action items
- Overall health status (On track / At risk / Critical)

### Jira sprint analysis
Connects to a Jira sprint and automatically produces:
- Sprint completion percentage
- Count of critical, blocked, and unassigned tickets
- Risk breakdown by ticket ID with assignee
- Prioritized action items for the PM

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Analysis | Custom rule-based NLP engine |
| Jira | Jira REST API (mock data for demo) |
| Deployment | Render (free tier) |

---

## How to run locally

### 1. Clone the repo
```
git clone https://github.com/YOUR-USERNAME/ai-project-dashboard.git
cd ai-project-dashboard
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the app
```
python app.py
```

Open your browser at `http://localhost:5000`

---

## Project structure
```
ai-project-dashboard/
├── index.html          # Frontend — tabbed dashboard UI
├── app.py              # Backend — Flask server + NLP engine
├── jira_connector.py   # Jira integration layer
├── mock_jira.py        # Realistic mock sprint data
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── .gitignore          # Files excluded from version control
└── README.md           # This file
```

---

## Connecting to real Jira

To connect to a live Jira project, open `jira_connector.py` and:

1. Set `USE_REAL_JIRA = True`
2. Fill in your credentials:
```python
JIRA_BASE_URL = "https://your-org.atlassian.net"
JIRA_EMAIL = "you@company.com"
JIRA_API_TOKEN = "your-token-here"
JIRA_PROJECT_KEY = "YOUR-PROJECT"
```
3. Generate your API token at: https://id.atlassian.com/manage-profile/security/api-tokens

No other code changes needed — the rest of the app works automatically.

---

## Roadmap

- [x] Rule-based NLP analysis engine
- [x] Risk detection and severity scoring
- [x] Action item extraction
- [x] Jira integration (mock data)
- [x] Deployed live on Render
- [x] CSV export of analysis results
- [ ] Power BI dashboard connected to CSV export
- [ ] Real Jira API connection
- [ ] AI API integration (Claude / Gemini) as optional enhancement
