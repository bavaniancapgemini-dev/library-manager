import sqlite3


def search_book(keyword):

    connection = sqlite3.connect("library.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ("%" + keyword + "%",)
    )

    results = cursor.fetchall()

    connection.close()

    return results