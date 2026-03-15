import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "/d3b4/usr/workdir/credentials.db"

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def verify_login(username, password):
    """Verify login credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM credentials WHERE username = ? AND password = ?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error verifying login: {e}")
        return False

def get_credentials():
    """Get current credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM credentials WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            return {"username": result[0], "password": result[1]}
        return None
    except Exception as e:
        print(f"Error getting credentials: {e}")
        return None

def update_credentials(username, password):
    """Update credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE credentials SET username = ?, password = ?, updated_at = ? WHERE id = 1",
            (username, password, datetime.now())
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating credentials: {e}")
        return False

def get_settings():
    """Get current settings"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT settings FROM credentials WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            return json.loads(result[0])
        return {}
    except Exception as e:
        print(f"Error getting settings: {e}")
        return {}

def update_settings(settings_dict):
    """Update settings"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        settings_json = json.dumps(settings_dict)
        cursor.execute(
            "UPDATE credentials SET settings = ?, updated_at = ? WHERE id = 1",
            (settings_json, datetime.now())
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating settings: {e}")
        return False
