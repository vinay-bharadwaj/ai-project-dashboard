from flask import Flask, request, jsonify, send_from_directory, Response
from jira_connector import get_tickets
import re
import json
import csv
import io
from datetime import datetime

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

@app.route('/jira-analyze', methods=['GET'])
def jira_analyze():
    data = get_tickets()
    tickets = data['tickets']

    all_risks = []
    all_actions = []
    seen_risks = set()

    critical_count = sum(
        1 for t in tickets if t['priority'] == 'Critical'
    )
    blocked_count = sum(
        1 for t in tickets if t['status'] == 'Blocked'
    )
    done_count = sum(
        1 for t in tickets if t['status'] == 'Done'
    )
    unassigned_count = sum(
        1 for t in tickets if t['assignee'] == 'Unassigned'
    )
    total = len(tickets)
    completion_pct = round((done_count / total) * 100) if total > 0 else 0

    for ticket in tickets:
        text = f"{ticket['summary']}. {ticket['description']}"
        level, keyword = classify_risk_ticket(ticket)
        if level and ticket['id'] not in seen_risks:
            all_risks.append({
                'level': level,
                'text': f"[{ticket['id']}] {ticket['summary']}",
                'id': ticket['id'],
                'status': ticket['status'],
                'assignee': ticket['assignee']
            })
            seen_risks.add(ticket['id'])

        if ticket['status'] in ['Blocked', 'To Do'] and \
           ticket['priority'] in ['Critical', 'High']:
            if ticket['assignee'] == 'Unassigned':
                all_actions.append(
                    f"Assign {ticket['id']} ({ticket['summary']}) immediately"
                )
            else:
                all_actions.append(
                    f"Unblock {ticket['id']} ({ticket['summary']}) "
                    f"— assigned to {ticket['assignee']}"
                )

    order = {'High': 0, 'Medium': 1, 'Low': 2}
    all_risks.sort(key=lambda x: order.get(x['level'], 3))
    all_risks = all_risks[:6]
    all_actions = all_actions[:5]

    if critical_count >= 2 or blocked_count >= 2:
        health = 'Critical'
    elif critical_count == 1 or blocked_count == 1 or \
         completion_pct < 40:
        health = 'At risk'
    else:
        health = 'On track'

    summary = (
        f"{data['project']} has {total} tickets with "
        f"{completion_pct}% completion. "
        f"{critical_count} critical ticket(s) and "
        f"{blocked_count} blocked ticket(s) require immediate attention. "
        f"{unassigned_count} ticket(s) are currently unassigned."
    )

    if not all_actions:
        all_actions = [
            "Review all unassigned tickets and allocate owners",
            "Send sprint status update to stakeholders",
            "Schedule daily standup to track critical items"
        ]

    return jsonify({
        'health': health,
        'summary': summary,
        'risks': all_risks,
        'actions': all_actions,
        'stats': {
            'total': total,
            'done': done_count,
            'completion_pct': completion_pct,
            'critical': critical_count,
            'blocked': blocked_count,
            'unassigned': unassigned_count
        },
        'project': data['project'],
        'sprint': data['sprint']
    })


def classify_risk_ticket(ticket):
    if ticket['priority'] == 'Critical' or ticket['status'] == 'Blocked':
        return 'High', ticket['priority']
    if ticket['priority'] == 'High' or ticket['status'] == 'In Progress' \
       and ticket['assignee'] == 'Unassigned':
        return 'Medium', ticket['priority']
    if ticket['priority'] == 'Medium':
        return 'Low', ticket['priority']
    return None, None

@app.route('/export-csv', methods=['POST'])
def export_csv():
    data = request.get_json()

    output = io.StringIO()
    writer = csv.writer(output)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    writer.writerow(['AI Project Status Dashboard — Export'])
    writer.writerow(['Generated on', timestamp])
    writer.writerow([])

    writer.writerow(['OVERALL HEALTH'])
    writer.writerow(['Status', data.get('health', '—')])
    writer.writerow([])

    writer.writerow(['SUMMARY'])
    writer.writerow([data.get('summary', '—')])
    writer.writerow([])

    writer.writerow(['RISKS'])
    writer.writerow(['Severity', 'Description'])
    for risk in data.get('risks', []):
        ticket_id = risk.get('id', '')
        text = f"[{ticket_id}] {risk['text']}" if ticket_id else risk['text']
        writer.writerow([risk['level'], text])
    writer.writerow([])

    writer.writerow(['ACTION ITEMS'])
    writer.writerow(['#', 'Action'])
    for i, action in enumerate(data.get('actions', []), 1):
        writer.writerow([i, action])
    writer.writerow([])

    if data.get('stats'):
        s = data['stats']
        writer.writerow(['SPRINT STATS'])
        writer.writerow(['Total tickets', s.get('total', '—')])
        writer.writerow(['Completed', s.get('done', '—')])
        writer.writerow(['Completion %', str(s.get('completion_pct', '—')) + '%'])
        writer.writerow(['Critical tickets', s.get('critical', '—')])
        writer.writerow(['Blocked tickets', s.get('blocked', '—')])
        writer.writerow(['Unassigned tickets', s.get('unassigned', '—')])

    filename = f"project_analysis_{datetime.now().strftime('%Y_%m_%d')}.csv"

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )

if __name__ == '__main__':
    app.run(debug=True)