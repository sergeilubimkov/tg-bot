import datetime
import sqlite3
def add_user(telegram_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,))
    conn.commit()
    conn.close()

def check_users(telegram_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = (?)", (telegram_id,))
    checking = cursor.fetchone() is not None
    conn.close()
    return checking

def add_expenses(telegram_id, amount, category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (telegram_id, amount, category) VALUES (?,?,?)",
                        (telegram_id, amount, category))
    conn.commit()
    conn.close()

def today_expenses(telegram_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount), category FROM expenses WHERE telegram_id = (?) AND DATE(created_at) = (?) GROUP BY category",
                   (telegram_id,datetime.date.today()))
    today_ex = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE telegram_id = (?) AND DATE(created_at) = (?)",
                   (telegram_id, datetime.date.today()))
    result = cursor.fetchone()
    if not today_ex:
        today_ex = []
    if result is None or result[0] is None:
        today_sum = 0
    else:
        today_sum = result[0]
    conn.close()
    return today_ex, today_sum