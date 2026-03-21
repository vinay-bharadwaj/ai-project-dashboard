# AI Project Status Dashboard

An AI-powered web app that analyzes project status updates and returns:
- A plain-English summary
- Flagged risks (High / Medium / Low)
- Recommended action items
- Overall project health status

## Tech stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **AI**: Anthropic Claude API

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

### 3. Add your API key
Create a file called `.env` and add:
```
ANTHROPIC_API_KEY=your_key_here
```

### 4. Run the app
```
python app.py
```

Open your browser at `http://localhost:5000`

## Project structure
```
ai-project-dashboard/
├── index.html        # Frontend dashboard UI
├── app.py            # Python/Flask backend server
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## About
Built as a portfolio project to demonstrate AI integration skills.
```
