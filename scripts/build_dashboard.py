import os
import json
from datetime import datetime
import glob

def build_dashboard():
    """Build HTML dashboard from meeting data"""
    
    # Read all parsed meeting data
    meetings = []
    os.makedirs('data/parsed_meetings', exist_ok=True)
    
    for json_file in glob.glob('data/parsed_meetings/*.json'):
        with open(json_file) as f:
            meetings.append(json.load(f))
    
    # Sort by date (newest first)
    meetings.sort(key=lambda x: x['date'], reverse=True)
    
    latest_meeting = meetings[0] if meetings else None
    
    # Generate HTML
    html = generate_html(meetings, latest_meeting)
    
    # Write to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Dashboard built successfully")
    if meetings:
        print(f"📊 Total meetings: {len(meetings)}")
        print(f"📅 Latest: {latest_meeting['meeting']}")


def generate_html(meetings, latest_meeting):
    """Generate complete HTML dashboard"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Meeting Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .timestamp {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        
        .card h2 {{
            color: #667eea;
            font-size: 1.3rem;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .meeting-header {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .meeting-title {{
            font-weight: bold;
            color: #333;
            font-size: 1.1rem;
        }}
        
        .meeting-date {{
            color: #666;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .action-item {{
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        
        .action-task {{
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .action-owner {{
            color: #667eea;
            font-size: 0.9rem;
            margin-bottom: 3px;
        }}
        
        .action-due {{
            color: #ff6b6b;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .risk-item {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
            color: #333;
        }}
        
        .summary {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            color: #333;
            line-height: 1.6;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        @media (max-width: 768px) {{
            .stats {{ grid-template-columns: 1fr; }}
            h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Team Meeting Dashboard</h1>
            <p class="timestamp">Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(meetings)}</div>
                <div class="stat-label">Total Meetings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(latest_meeting['action_items']) if latest_meeting else 0}</div>
                <div class="stat-label">Active Action Items</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(latest_meeting['risks']) if latest_meeting else 0}</div>
                <div class="stat-label">Identified Risks</div>
            </div>
        </div>
"""
    
    if latest_meeting:
        html += f"""
        <div class="card">
            <h2>📅 Latest Meeting</h2>
            <div class="meeting-header">
                <div class="meeting-title">{latest_meeting['meeting']}</div>
                <div class="meeting-date">📆 {latest_meeting['date']}</div>
                <div class="meeting-date">👥 {', '.join(latest_meeting['attendees'])}</div>
            </div>
            
            <div class="summary">
                {latest_meeting['summary']}
            </div>
        </div>
        
        <div class="card">
            <h2>✅ Decisions Made</h2>
"""
        if latest_meeting['decisions']:
            for decision in latest_meeting['decisions']:
                html += f'<div style="padding: 10px; background: #e8f5e9; border-left: 4px solid #4caf50; margin-bottom: 10px; border-radius: 4px;">✓ {decision}</div>'
        else:
            html += "<p>No decisions recorded</p>"
        
        html += """
        </div>
        
        <div class="card">
            <h2>📋 Action Items</h2>
"""
        if latest_meeting['action_items']:
            for item in latest_meeting['action_items']:
                html += f"""
            <div class="action-item">
                <div class="action-task">• {item['task']}</div>
                <div class="action-owner">👤 Owner: {item['owner']}</div>
                <div class="action-due">📅 Due: {item['due']}</div>
            </div>
"""
        else:
            html += "<p>No action items</p>"
        
        html += """
        </div>
        
        <div class="card">
            <h2>⚠️ Risks Identified</h2>
"""
        if latest_meeting['risks']:
            for risk in latest_meeting['risks']:
                html += f'<div class="risk-item">⚠️ {risk}</div>'
        else:
            html += "<p>No risks identified</p>"
        
        html += """
        </div>
"""
    
    html += """
        <footer>
            <p>🤖 This dashboard is auto-generated by GitHub Actions</p>
            <p>📝 Meeting notes are archived in the repository</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == "__main__":
    build_dashboard()
