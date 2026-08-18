import json
import os
import subprocess
import glob

def create_issues():
    """Create GitHub Issues for each action item"""
    
    json_file = get_latest_meeting_json()
    if not json_file:
        print("❌ No meeting data found")
        return
    
    with open(json_file, encoding='utf-8') as f:
        meeting = json.load(f)
    
    print(f"📋 Creating issues for: {meeting['meeting']}")
    
    if not meeting['action_items']:
        print("⚠️ No action items to create")
        return
    
    created_count = 0
    for item in meeting['action_items']:
        if create_github_issue(
            title=f"[ACTION] {item['task']}",
            body=f"""**Meeting:** {meeting['meeting']}
**Date:** {meeting['date']}
**Owner:** {item['owner']}
**Due Date:** {item['due']}

---

From meeting notes: {meeting['summary'][:200]}...

[View Dashboard](https://github.com)
            """,
            assignee=item['owner'].lower().replace(' ', ''),
            labels=['action-item', 'meeting-follow-up']
        ):
            created_count += 1
    
    print(f"✅ Created {created_count} issues")


def create_github_issue(title, body, assignee, labels):
    """Create a single GitHub Issue using GitHub CLI"""
    
    cmd = [
        'gh', 'issue', 'create',
        '--title', title,
        '--body', body,
    ]
    
    for label in labels:
        cmd.extend(['--label', label])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"✅ Created issue: {title}")
            return True
        else:
            print(f"⚠️ Could not create issue: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️ Error creating issue: {e}")
        return False


def get_latest_meeting_json():
    """Get the most recent parsed meeting JSON file"""
    files = sorted(glob.glob('data/parsed_meetings/*.json'), reverse=True)
    return files[0] if files else None


if __name__ == "__main__":
    create_issues()