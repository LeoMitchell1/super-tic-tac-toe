import sqlite3
from pathlib import Path

DB_PATH = Path("src\game\data\leaderboard.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_score(username, score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO leaderboard (player_name, score)
        VALUES (?, ?)
    ''', (username, score))

    conn.commit()
    conn.close()

def get_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT player_name, score
        FROM leaderboard
        ORDER BY score DESC
        LIMIT 10
    ''')

    results = cursor.fetchall()
    conn.close()
    return results

def get_usernames() -> set[str]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_name
        FROM leaderboard
    """)

    usernames = {row[0] for row in cursor.fetchall()}
    conn.close()
    return usernames

def clear_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM leaderboard')

    conn.commit()
    conn.close()

