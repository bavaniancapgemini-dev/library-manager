import sqlite3

def library_statistics():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")

    total_books = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM members")

    total_members = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Available'"
    )

    available_books = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Borrowed'"
    )

    borrowed_books = cursor.fetchone()[0]

    conn.close()

    return (
        total_books,
        total_members,
        available_books,
        borrowed_books
    )