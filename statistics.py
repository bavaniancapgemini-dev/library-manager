import sqlite3

def monthly_borrows():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        substr(borrow_date,1,7),

        COUNT(*)

        FROM transactions

        GROUP BY substr(borrow_date,1,7)

        ORDER BY substr(borrow_date,1,7)

    """)

    data = cursor.fetchall()

    conn.close()

    return data