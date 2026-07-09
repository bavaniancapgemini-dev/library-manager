import sqlite3

def active_members():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    member_name,

    COUNT(*)

    FROM transactions

    GROUP BY member_name

    ORDER BY COUNT(*) DESC

    LIMIT 10

    """)

    data = cursor.fetchall()

    conn.close()

    return data