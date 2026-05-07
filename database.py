import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    description TEXT,
    severity TEXT,
    status TEXT,
    timestamp TEXT,
    source_ip TEXT,
    user_id INTEGER,
    comments TEXT
)
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        enabled INTEGER
)
""")
    

    conn.commit()
    conn.close()
    
def create_default_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    rules = [
        ("Brute Force", 1),
        ("Port Scan", 1),
        ("File Access", 1),
        ("Unknown IP", 1)
    ]

    for name, enabled in rules:
        cursor.execute("SELECT * FROM rules WHERE name=?", (name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO rules (name, enabled) VALUES (?, ?)", (name, enabled))

    conn.commit()
    conn.close()


def create_default_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("admin", generate_password_hash("admin"), "Administrator"))

    # Analyst
    cursor.execute("SELECT * FROM users WHERE username='analyst'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("analyst", generate_password_hash("analyst"), "Security Analyst"))

    conn.commit()
    conn.close()


def add_incident(event_type, description, severity, source_ip="unknown", user_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO incidents 
    (event_type, description, severity, status, timestamp, source_ip, user_id, comments)
    VALUES (?, ?, ?, 'New', datetime('now'), ?, ?, '')
    """, (event_type, description, severity, source_ip, user_id))

    conn.commit()
    conn.close()


def get_incidents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data

def get_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM rules WHERE enabled=1")
    rules = [r[0] for r in cursor.fetchall()]

    conn.close()
    return rules


def clear_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM incidents")

    conn.commit()
    conn.close()