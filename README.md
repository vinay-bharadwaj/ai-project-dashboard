# AI Project Status Dashboard

An intelligent web app that analyzes project status updates and instantly returns:

- A plain-English summary
- Flagged risks (High / Medium / Low)
- Recommended action items
- Overall project health (On track / At risk / Critical)

## How it works

This project uses a **rule-based NLP engine** built entirely in Python —
no external AI APIs, no cost, no rate limits. The analyzer scans project
updates for risk keywords, scores sentences by severity, and generates
structured output. This makes it fast, predictable, and easy to extend.

## Tech stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Analysis**: Custom NLP engine (rule-based keyword scoring)

## How to run locally

### 1. Clone the repo
```
git clone https://github.com/YOUR-USERNAME/ai-project-dashboard.git
cd ai-project-dashboard
```

### 2. Install dependencies
```
pip install flask
```

### 3. Run the app
```
python app.py
```

Open your browser at `http://localhost:5000`

## Project structure
```
ai-project-dashboard/
├── index.html        # Frontend dashboard UI
├── app.py            # Python/Flask backend + NLP analysis engine
├── requirements.txt  # Python dependencies
├── .gitignore        # Files excluded from version control
└── README.md         # This file
```

## Roadmap

- [x] Rule-based NLP analysis engine
- [x] Risk detection and severity scoring
- [x] Action item extraction
- [ ] Jira integration to fetch and analyze tickets automatically
- [ ] AI API integration (Claude / Gemini) as optional enhancement
- [ ] Export analysis as PDF report
