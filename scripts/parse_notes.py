import re
import json
import os
import glob
from datetime import datetime

def parse_notes():
    """Parse all meeting notes files"""
    
    # Find all meeting notes files
    note_files = glob.glob('meeting-notes-*.txt')
    
    if not note_files:
        print("❌ No meeting notes files found")
        return
    
    # Process the latest file
    latest_file = max(note_files, key=os.path.getctime)
    
    with open(latest_file, encoding='utf-8') as f:
        content = f.read()
    
    data = {
        'meeting': extract_section(content, 'MEETING'),
        'date': extract_section(content, 'DATE'),
        'attendees': [x.strip() for x in extract_section(content, 'ATTENDEES').split(',')],
        'summary': extract_section(content, 'MEETING SUMMARY'),
        'decisions': extract_list(content, 'DECISIONS MADE'),
        'action_items': parse_action_items(content),
        'risks': extract_list(content, 'RISKS IDENTIFIED'),
        'next_steps': extract_section(content, 'NEXT STEPS'),
        'timestamp': datetime.now().isoformat()
    }
    
    # Save to JSON for dashboard to read
    os.makedirs('data/parsed_meetings', exist_ok=True)
    json_file = f"data/parsed_meetings/{data['date'].replace('-', '_')}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Parsed: {data['meeting']}")
    print(f"📋 Action items: {len(data['action_items'])}")
    print(f"⚠️ Risks: {len(data['risks'])}")
    
    return data


def extract_section(content, section_name):
    """Extract text between section header and next section"""
    pattern = f"{section_name}.*?:(.*?)(?=^[A-Z][A-Z ]+:|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_list(content, section_name):
    """Extract bulleted list from a section"""
    section = extract_section(content, section_name)
    items = [line.strip('- ').strip() for line in section.split('\n') if line.strip().startswith('-')]
    return items


def parse_action_items(content):
    """Parse action items with owner and due date"""
    section = extract_section(content, 'ACTION ITEMS')
    items = []
    
    lines = section.split('\n')
    for line in lines:
        if line.strip().startswith('-'):
            # Format: "- Sarah: Create spec by Jan 20"
            item_text = line.strip('- ').strip()
            
            # Extract owner (person before the colon)
            owner_match = re.match(r"^([^:]+):\s*(.*?)(?:\s+by\s+(.+))?$", item_text)
            if owner_match:
                owner = owner_match.group(1).strip()
                task = owner_match.group(2).strip()
                due = owner_match.group(3).strip() if owner_match.group(3) else "TBD"
                
                items.append({
                    'task': task,
                    'owner': owner,
                    'due': due
                })
    
    return items


if __name__ == "__main__":
    parse_notes()