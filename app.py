from flask import Flask, request, jsonify, send_from_directory
import re
import json

app = Flask(__name__)

HIGH_RISK_KEYWORDS = [
    'critical', 'blocker', 'blocked', 'showstopper', 'urgent',
    'failed', 'failure', 'crash', 'down', 'outage', 'broken',
    'cannot', "can't", 'unable', 'impossible', 'escalate',
    'overdue', 'missed deadline', 'missed launch', 'at risk'
]

MEDIUM_RISK_KEYWORDS = [
    'delay', 'delayed', 'behind', 'slow', 'slipping', 'slipped',
    'concern', 'issue', 'problem', 'bug', 'defect', 'error',
    'dependency', 'waiting', 'pending', 'unclear', 'unknown',
    'missing', 'gap', 'risk', 'challenge', 'difficult', 'struggle'
]

LOW_RISK_KEYWORDS = [
    'minor', 'small', 'slight', 'note', 'fyi', 'heads up',
    'watch', 'monitor', 'tracking', 'aware', 'flagging'
]

ACTION_TRIGGER_WORDS = [
    'need', 'needs', 'required', 'must', 'should', 'have to',
    'waiting for', 'pending', 'follow up', 'follow-up', 'action',
    'assign', 'resolve', 'fix', 'update', 'schedule', 'confirm',
    'review', 'approve', 'escalate', 'send', 'share', 'complete'
]

PROGRESS_KEYWORDS = [
    'complete', 'completed', 'done', 'finished', 'delivered',
    'launched', 'shipped', 'released', 'on track', 'on schedule',
    'good', 'great', 'excellent', 'ahead', 'progressing'
]

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    return sentences

def classify_risk(sentence):
    sentence_lower = sentence.lower()
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in sentence_lower:
            return 'High', keyword
    for keyword in MEDIUM_RISK_KEYWORDS:
        if keyword in sentence_lower:
            return 'Medium', keyword
    for keyword in LOW_RISK_KEYWORDS:
        if keyword in sentence_lower:
            return 'Low', keyword
    return None, None

def is_action_item(sentence):
    sentence_lower = sentence.lower()
    for trigger in ACTION_TRIGGER_WORDS:
        if trigger in sentence_lower:
            return True
    return False

def calculate_health(risks):
    if not risks:
        return 'On track'
    high_count = sum(1 for r in risks if r['level'] == 'High')
    medium_count = sum(1 for r in risks if r['level'] == 'Medium')
    if high_count >= 2:
        return 'Critical'
    elif high_count == 1 or medium_count >= 2:
        return 'At risk'
    else:
        return 'On track'

def generate_summary(sentences, risks, health):
    total = len(sentences)
    risk_count = len(risks)
    high_risks = [r for r in risks if r['level'] == 'High']
    progress_sentences = [
        s for s in sentences
        if any(p in s.lower() for p in PROGRESS_KEYWORDS)
    ]
    summary_parts = []
    if progress_sentences:
        summary_parts.append(progress_sentences[0])
    if high_risks:
        summary_parts.append(
            f"Key concern: {high_risks[0]['text'].lower()}"
        )
    if health == 'Critical':
        summary_parts.append(
            "Immediate action is required to get the project back on track."
        )
    elif health == 'At risk':
        summary_parts.append(
            "The project needs attention to avoid further delays."
        )
    else:
        summary_parts.append(
            "The project is progressing well with no major blockers."
        )
    return ' '.join(summary_parts) if summary_parts else \
        "Project update analyzed. Review risks and action items below."

def generate_actions(sentences, risks):
    actions = []
    seen = set()
    for sentence in sentences:
        if is_action_item(sentence) and sentence not in seen:
            clean = sentence.strip().rstrip('.')
            if len(clean) > 15 and len(actions) < 5:
                actions.append(clean)
                seen.add(sentence)
    if not actions and risks:
        for risk in risks[:3]:
            if risk['level'] == 'High':
                actions.append(
                    f"Immediately address: {risk['text']}"
                )
            elif risk['level'] == 'Medium':
                actions.append(
                    f"Create a plan to resolve: {risk['text']}"
                )
    if not actions:
        actions.append("Review project timeline with the team")
        actions.append("Send a status update to stakeholders")
    return actions

def analyze_text(text):
    sentences = split_sentences(text)
    risks = []
    seen_risks = set()
    for sentence in sentences:
        level, keyword = classify_risk(sentence)
        if level and sentence not in seen_risks:
            risks.append({
                'level': level,
                'text': sentence.strip()
            })
            seen_risks.add(sentence)
    order = {'High': 0, 'Medium': 1, 'Low': 2}
    risks.sort(key=lambda x: order[x['level']])
    risks = risks[:4]
    health = calculate_health(risks)
    summary = generate_summary(sentences, risks, health)
    actions = generate_actions(sentences, risks)
    return {
        'health': health,
        'summary': summary,
        'risks': risks,
        'actions': actions
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    project_text = data.get('text', '')
    if not project_text:
        return jsonify({'error': 'No text provided'}), 400
    result = analyze_text(project_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)