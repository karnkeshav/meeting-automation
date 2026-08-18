import json
import os
import requests
import glob
from datetime import datetime

def send_teams_notification():
    """Send formatted message to Microsoft Teams"""
    
    # Read the latest parsed meeting data
    json_file = get_latest_meeting_json()
    if not json_file:
        print("❌ No meeting data found")
        return
    
    with open(json_file, encoding='utf-8') as f:
        meeting = json.load(f)
    
    # Get Teams webhook URL from GitHub secrets
    teams_webhook = os.getenv('TEAMS_WEBHOOK')
    if not teams_webhook:
        print("⚠️ TEAMS_WEBHOOK not set - skipping Teams notification")
        return
    
    # Build Teams message
    message = build_teams_message(meeting)
    
    # Send to Teams
    try:
        response = requests.post(teams_webhook, json=message)
        
        if response.status_code == 200:
            print("✅ Message sent to Microsoft Teams")
        else:
            print(f"⚠️ Teams response: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error sending to Teams: {e}")


def build_teams_message(meeting):
    """Build adaptive card for Microsoft Teams"""
    
    # Build facts for action items
    action_facts = []
    for item in meeting['action_items'][:5]:
        action_facts.append({
            "name": f"{item['owner']}",
            "value": f"{item['task']} (Due: {item['due']})"
        })
    
    # Build facts for decisions
    decision_facts = []
    for i, decision in enumerate(meeting['decisions'][:3], 1):
        decision_facts.append({
            "name": f"Decision {i}",
            "value": decision
        })
    
    # Build facts for risks
    risk_facts = []
    for i, risk in enumerate(meeting['risks'][:3], 1):
        risk_facts.append({
            "name": f"Risk {i}",
            "value": risk
        })
    
    # Build complete message
    sections = [
        {
            "activityTitle": f"📊 {meeting['meeting']}",
            "activitySubtitle": f"📆 {meeting['date']} | 👥 {', '.join(meeting['attendees'])}",
            "text": meeting['summary'],
            "markdown": True
        }
    ]
    
    if decision_facts:
        sections.append({
            "activityTitle": "✅ Decisions Made",
            "facts": decision_facts
        })
    
    if action_facts:
        sections.append({
            "activityTitle": "📋 Action Items",
            "facts": action_facts
        })
    
    if risk_facts:
        sections.append({
            "activityTitle": "⚠️ Risks Identified",
            "facts": risk_facts
        })
    
    message = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": f"Meeting Notes - {meeting['meeting']}",
        "themeColor": "667eea",
        "sections": sections,
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "View Dashboard",
                "targets": [{"os": "default", "uri": "https://github.com"}]
            },
            {
                "@type": "OpenUri",
                "name": "View on GitHub",
                "targets": [{"os": "default", "uri": "https://github.com"}]
            }
        ]
    }
    
    return message


def get_latest_meeting_json():
    """Get the most recent parsed meeting JSON file"""
    files = sorted(glob.glob('data/parsed_meetings/*.json'), reverse=True)
    return files[0] if files else None


if __name__ == "__main__":
    send_teams_notification()