import os
import psycopg2

conn = psycopg2.connect(
    host = os.getenv("DB_HOST", "localhost"),
    database = os.getenv("DB_NAME", "expenses_db"),
    user = os.getenv("DB_USER", "botuser"),
    password = os.getenv("DB_PASSWORD", "botpass")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users
(
    telegram_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses 
(
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    amount REAL NOT NULL,
    category VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()