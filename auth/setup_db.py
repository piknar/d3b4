import sqlite3
import os

db_path = "/d3b4/usr/workdir/credentials.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    settings TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
INSERT OR REPLACE INTO credentials (id, username, password, settings)
VALUES (1, 'piknar', 'piknar', '{"theme": "dark", "language": "en", "notifications": true}')
''')

conn.commit()
conn.close()
print(f"Database initialized at {db_path}")
