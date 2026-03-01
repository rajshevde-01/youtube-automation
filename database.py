import sqlite3
import os
from datetime import datetime

DB_PATH = "youtube_automation.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_date TEXT,
            topic TEXT,
            video_title TEXT,
            status TEXT,
            youtube_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def has_uploaded_today():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM uploads WHERE upload_date = ? AND status = 'SUCCESS'", (today,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def log_upload(topic, video_title, status, youtube_url=""):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uploads (upload_date, topic, video_title, status, youtube_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (today, topic, video_title, status, youtube_url))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
