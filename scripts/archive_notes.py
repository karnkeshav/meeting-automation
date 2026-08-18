import os
import shutil
import glob
from datetime import datetime

def archive_notes():
    """Archive meeting notes to historical folder"""
    
    # Find latest meeting notes file
    files = glob.glob('meeting-notes-*.txt')
    
    if not files:
        print("⚠️ No meeting notes to archive")
        return
    
    latest_file = max(files, key=os.path.getctime)
    
    # Get date from filename
    date_str = latest_file.replace('meeting-notes-', '').replace('.txt', '')
    
    # Create archive folder (YYYY/MM format)
    archive_dir = f"archives/{date_str[:7]}"  # YYYY-MM
    os.makedirs(archive_dir, exist_ok=True)
    
    # Move file
    dest = f"{archive_dir}/{latest_file}"
    
    if os.path.exists(dest):
        print(f"⚠️ File already archived: {dest}")
        return
    
    try:
        shutil.copy(latest_file, dest)
        print(f"📦 Archived: {dest}")
    except Exception as e:
        print(f"❌ Error archiving: {e}")


if __name__ == "__main__":
    archive_notes()