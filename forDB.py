import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users
(
    telegram_id INTEGER PRIMARY KEY,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()