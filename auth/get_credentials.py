import sqlite3
import json
import sys
sys.path.insert(0, '/d3b4/usr/workdir')
from auth_module import get_credentials, get_settings

if __name__ == '__main__':
    creds = get_credentials()
    settings = get_settings()
    
    if creds:
        print(f"Username: {creds['username']}")
        print(f"Password: {creds['password']}")
        print(f"Settings: {json.dumps(settings, indent=2)}")
    else:
        print("No credentials found")
