import os
import psycopg2
from datetime import date, timedelta
def get_conn():
    return psycopg2.connect(
        host = os.getenv("DB_HOST", "localhost"),
        database = os.getenv("DB_NAME", "expenses_db"),
        user = os.getenv("DB_USER", "botuser"),
        password = os.getenv("DB_PASSWORD", "botpass")
    )

def add_user(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,))
    conn.commit()
    conn.close()

def check_users(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""SELECT 1 
                        FROM users 
                        WHERE telegram_id = (%s)""", (telegram_id,))
    checking = cursor.fetchone() is not None
    conn.close()
    return checking

def add_expenses(telegram_id, amount, category):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (telegram_id, amount, category) VALUES (%s,%s,%s)",
                        (telegram_id, amount, category))
    conn.commit()
    conn.close()

def today_expenses(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""SELECT SUM(amount), category
                        FROM expenses 
                        WHERE telegram_id = (%s) AND DATE(created_at) = (%s) 
                        GROUP BY category""",
                   (telegram_id,date.today()))
    today_ex = cursor.fetchall()
    cursor.execute("""SELECT SUM(amount) 
                        FROM expenses 
                        WHERE telegram_id = (%s) AND DATE(created_at) = (%s)""",
                   (telegram_id, date.today()))
    result = cursor.fetchone()
    if not today_ex:
        today_ex = []
    if result is None or result[0] is None:
        today_sum = 0
    else:
        today_sum = result[0]
    conn.close()
    return today_ex, today_sum

def yesterday_expenses(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""SELECT SUM(amount), category 
                        FROM expenses 
                        WHERE telegram_id = (%s) AND DATE(created_at) = (%s) 
                        GROUP BY category""",
                   (telegram_id, date.today() - timedelta(days=1)))
    yesterday_ex = cursor.fetchall()
    cursor.execute("""SELECT SUM(amount) 
                        FROM expenses 
                        WHERE telegram_id = (%s) AND DATE(created_at) = (%s)""",
                   (telegram_id, date.today() - timedelta(days=1)))
    result = cursor.fetchone()
    if not yesterday_ex:
        yesterday_ex = []
    if result is None or result[0] is None:
        yesterday_sum = 0
    else:
        yesterday_sum = result[0]
    conn.close()
    return yesterday_ex, yesterday_sum


def week_expenses(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    cursor.execute(
        """SELECT SUM(amount), category 
            FROM expenses 
            WHERE telegram_id = (%s) AND DATE(created_at) BETWEEN %s AND %s 
            GROUP BY category""",
        (telegram_id, start_date, end_date))
    week_expense = cursor.fetchall()
    cursor.execute("""SELECT SUM(amount) 
                            FROM expenses 
                            WHERE telegram_id = (%s) AND DATE(created_at) BETWEEN %s AND %s""",
                   (telegram_id, start_date, end_date))
    result = cursor.fetchone()
    if not week_expense:
        week_expense = []
    if result is None or result[0] is None:
        week_sum = 0
    else:
        week_sum = result[0]
    conn.close()
    return week_expense, week_sum


def month_expenses(telegram_id):
    conn = get_conn()
    cursor = conn.cursor()
    start_date = date.today().replace(day=1)
    end_date = date.today()
    cursor.execute(
        """SELECT SUM(amount), category 
            FROM expenses 
            WHERE telegram_id = (%s) AND DATE(created_at) BETWEEN %s AND %s 
            GROUP BY category""",
        (telegram_id, start_date, end_date))
    month_expense = cursor.fetchall()
    cursor.execute("""SELECT SUM(amount) 
                            FROM expenses 
                            WHERE telegram_id = (%s) AND DATE(created_at) BETWEEN %s AND %s""",
                   (telegram_id, start_date, end_date))
    result = cursor.fetchone()
    if not month_expense:
        month_expense = []
    if result is None or result[0] is None:
        month_sum = 0
    else:
        month_sum = result[0]
    conn.close()
    return month_expense, month_sum

def getUsers():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT telegram_id
            FROM users""",
        )
    result = cursor.fetchall()
    if not result:
        result = []
    conn.close()
    return [row[0] for row in result]