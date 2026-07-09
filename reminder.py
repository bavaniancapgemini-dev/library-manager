import sqlite3
from datetime import datetime

def due_today():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""

    SELECT

    book_title,

    member_name

    FROM transactions

    WHERE due_date=?

    AND return_date=''

    """,(today,))

    data = cursor.fetchall()

    conn.close()

    return data