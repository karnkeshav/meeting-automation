import json
import os
import requests
import glob

def create_issues():
    """Create GitHub Issues using GitHub REST API"""
    
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
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️ GITHUB_TOKEN not set - skipping issue creation")
        return
    
    # Get repo info from environment
    github_repo = os.getenv('GITHUB_REPOSITORY', 'karnkeshav/meeting-automation')
    
    created_count = 0
    for item in meeting['action_items']:
        if create_github_issue(
            token=github_token,
            repo=github_repo,
            title=f"[ACTION] {item['task']}",
            body=f"""**Meeting:** {meeting['meeting']}
**Date:** {meeting['date']}
**Owner:** {item['owner']}
**Due Date:** {item['due']}

---

From meeting notes: {meeting['summary'][:200]}...
            """,
            labels=['action-item', 'meeting-follow-up']
        ):
            created_count += 1
    
    print(f"✅ Created {created_count} issues")


def create_github_issue(token, repo, title, body, labels):
    """Create a GitHub Issue using REST API"""
    
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            issue_num = response.json()['number']
            print(f"✅ Created issue #{issue_num}: {title}")
            return True
        else:
            print(f"⚠️ Issue creation failed: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:100]}")
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
