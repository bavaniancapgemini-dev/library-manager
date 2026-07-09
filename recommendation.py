import sqlite3

def recommend_books(category):

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title,
               author
        FROM books
        WHERE category=?
        AND status='Available'
        LIMIT 5
        """,
        (category,)
    )

    books = cursor.fetchall()

    conn.close()

    return books