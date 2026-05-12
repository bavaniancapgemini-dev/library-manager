import sqlite3


connection = sqlite3.connect("library.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    title TEXT,
    author TEXT
)
""")

connection.commit()

connection.close()

def add_book(title, author):

    connection = sqlite3.connect("library.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books VALUES (?, ?)",
        (title, author)
    )

    connection.commit()

    connection.close()

def view_books():

    connection = sqlite3.connect("library.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return books

def delete_book(title):

    connection = sqlite3.connect("library.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM books WHERE title=?",
        (title,)
    )

    connection.commit()

    connection.close()