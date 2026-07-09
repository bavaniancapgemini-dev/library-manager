from datetime import datetime, timedelta
import sqlite3

connection = sqlite3.connect("library.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(

id INTEGER PRIMARY KEY AUTOINCREMENT,

title TEXT,

author TEXT,

isbn TEXT UNIQUE,

category TEXT,

status TEXT,

borrowed_by TEXT,

borrow_date TEXT,

due_date TEXT,

copies INTEGER

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    member_name TEXT,
    rating INTEGER,
    review TEXT
)
""")

connection.commit()

connection.commit()

connection.close()

def add_book(title, author, isbn, category, copies):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO books(

        title,

        author,

        isbn,

        category,

        status,

        borrowed_by,

        copies

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            title,

            author,

            isbn,

            category,

            "Available",

            "",

            copies

        )

    )

    conn.commit()

    conn.close()

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
    
def available_books():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM books WHERE status='Available'"

    )

    books = cursor.fetchall()

    conn.close()

    return books

def borrowed_books():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM books WHERE status='Borrowed'"

    )

    books = cursor.fetchall()

    conn.close()

    return books

def update_status(title, status):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "UPDATE books SET status=? WHERE title=?",

        (status, title)
        
    )

    conn.commit()

    conn.close()
    
def create_member_table():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS members(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT

    )

    """)

    conn.commit()

    conn.close()
    

def add_member(name, phone):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO members(name,phone) VALUES(?,?)",

        (name, phone)

    )

    conn.commit()

    conn.close()
    
def view_members():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM members"

    )

    members = cursor.fetchall()

    conn.close()

    return members

def search_member(keyword):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM members WHERE name LIKE ?",

        ("%"+keyword+"%",)

    )

    data = cursor.fetchall()

    conn.close()

    return data

def total_members():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM members"

    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def borrow_book(title, member):

    import sqlite3

    from datetime import datetime, timedelta

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    borrow_date = datetime.now()

    due_date = borrow_date + timedelta(days=14)

    cursor.execute(
        """
        UPDATE books
        SET
            status=?,
            borrowed_by=?,
            borrow_date=?,
            due_date=?
        WHERE title=?
        """,
        (
            "Borrowed",
            member,
            borrow_date.strftime("%Y-%m-%d"),
            due_date.strftime("%Y-%m-%d"),
            title
        )
    )

    conn.commit()

    conn.close()
    
def return_book(title):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET
            status=?,
            borrowed_by='',
            borrow_date='',
            due_date=''
        WHERE title=?
        """,
        (
            "Available",
            title
        )
    )

    conn.commit()

    conn.close()
    
def create_transaction_table():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        book_title TEXT,

        member_name TEXT,

        borrow_date TEXT,

        due_date TEXT,

        return_date TEXT

    )

    """)

    conn.commit()

    conn.close()
    
def return_book(title):

    import sqlite3

    from datetime import datetime

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET status=?,
            borrowed_by=?
        WHERE title=?
        """,
        (
            "Available",
            "",
            title
        )
    )

    cursor.execute(
        """
        UPDATE transactions
        SET return_date=?
        WHERE book_title=? AND return_date=''
        """,
        (
            datetime.now().strftime("%Y-%m-%d"),
            title
        )
    )

    conn.commit()

    conn.close()
    
def view_transactions(): 
    
    import sqlite3 
    
    conn = sqlite3.connect("library.db") 
    
    cursor = conn.cursor() 
    
    cursor.execute( "SELECT * FROM transactions" ) 
    
    data = cursor.fetchall() 
    
    conn.close() 
    
    return data
    
def overdue_books():

    import sqlite3

    from datetime import datetime

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT *
        FROM transactions
        WHERE due_date<?
        AND return_date=''
        """,
        (today,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

from datetime import datetime

def calculate_fine():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT book_title,
               member_name,
               due_date
        FROM transactions
        WHERE return_date=''
    """)

    rows = cursor.fetchall()

    conn.close()

    fines = []

    today = datetime.now()

    for row in rows:

        due = datetime.strptime(row[2], "%Y-%m-%d")

        if today > due:

            overdue = (today - due).days

            fine = overdue * 10

            fines.append(

                (

                    row[0],
                    row[1],
                    overdue,
                    fine

                )

            )

    return fines

def dashboard():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")

    total_books = cursor.fetchone()[0]

    cursor.execute(

        "SELECT COUNT(*) FROM books WHERE status='Available'"

    )

    available = cursor.fetchone()[0]

    cursor.execute(

        "SELECT COUNT(*) FROM books WHERE status='Borrowed'"

    )

    borrowed = cursor.fetchone()[0]

    cursor.execute(

        "SELECT COUNT(*) FROM members"

    )

    members = cursor.fetchone()[0]

    conn.close()

    return (

        total_books,

        available,

        borrowed,

        members

    )
    
def most_borrowed():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        book_title,

        COUNT(*)

    FROM transactions

    GROUP BY book_title

    ORDER BY COUNT(*) DESC

    LIMIT 5

    """)

    data = cursor.fetchall()

    conn.close()

    return data

import csv

def export_transactions():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM transactions"

    )

    rows = cursor.fetchall()

    conn.close()

    with open(

        "transactions.csv",

        "w",

        newline=""

    ) as file:

        writer = csv.writer(file)

        writer.writerow(

            [

                "ID",

                "Book",

                "Member",

                "Borrow Date",

                "Due Date",

                "Return Date"

            ]

        )

        writer.writerows(rows)
        
def create_reservation_table():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS reservations(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    member_name TEXT,

    book_title TEXT,

    reservation_date TEXT

    )

    """)

    conn.commit()

    conn.close()
    
from datetime import datetime

def reserve_book(member, book):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO reservations(

        member_name,

        book_title,

        reservation_date

        )

        VALUES(?,?,?)

        """,

        (

            member,

            book,

            datetime.now().strftime("%Y-%m-%d")

        )

    )

    conn.commit()

    conn.close()
    
def view_reservations():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM reservations"

    )

    data = cursor.fetchall()

    conn.close()

    return data

def restock_book(title, qty):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        UPDATE books

        SET copies=copies+?

        WHERE title=?

        """,

        (

            qty,

            title

        )

    )

    conn.commit()

    conn.close()
    
def low_stock():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE copies<=2

        """

    )

    data = cursor.fetchall()

    conn.close()

    return data

def update_book(book_id, title, author, category, copies):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET
            title=?,
            author=?,
            category=?,
            copies=?
        WHERE id=?
        """,
        (
            title,
            author,
            category,
            copies,
            book_id
        )
    )

    conn.commit()

    conn.close()
    
def delete_book_by_id(book_id):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM books WHERE id=?",

        (book_id,)

    )

    conn.commit()

    conn.close()
    
def search_books(keyword):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE title LIKE ?

        """,

        ("%"+keyword+"%",)

    )

    data = cursor.fetchall()

    conn.close()

    return data

def search_author(author):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE author LIKE ?

        """,

        ("%"+author+"%",)

    )

    data = cursor.fetchall()

    conn.close()

    return data

def search_category(category):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE category LIKE ?

        """,

        ("%"+category+"%",)

    )

    data = cursor.fetchall()

    conn.close()

    return data

def available_books():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE status='Available'

        """

    )

    data = cursor.fetchall()

    conn.close()

    return data

def borrowed_books():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM books

        WHERE status='Borrowed'

        """

    )

    data = cursor.fetchall()

    conn.close()

    return data

def dashboard_data():

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Available'"
    )
    available = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Borrowed'"
    )
    borrowed = cursor.fetchone()[0]

    conn.close()

    return (
        total_books,
        total_members,
        available,
        borrowed
    )

def calculate_fine(due_date):

    from datetime import datetime

    if due_date == "":
        return 0

    due = datetime.strptime(due_date, "%Y-%m-%d")

    today = datetime.now()

    if today <= due:
        return 0

    days = (today - due).days

    return days * 10

def overdue_books():

    import sqlite3

    from datetime import datetime

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE status='Borrowed'
        """
    )

    books = cursor.fetchall()

    overdue = []

    today = datetime.now()

    for book in books:

        if book[7]:

            due = datetime.strptime(book[7], "%Y-%m-%d")

            if today > due:

                overdue.append(book)

    conn.close()

    return overdue

def add_review(book_title, member_name, rating, review):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reviews
        (book_title, member_name, rating, review)
        VALUES(?,?,?,?)
        """,
        (book_title, member_name, rating, review)
    )

    conn.commit()

    conn.close()
    
def view_reviews(book_title):

    import sqlite3

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT member_name,
               rating,
               review
        FROM reviews
        WHERE book_title=?
        """,
        (book_title,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

def search_isbn(isbn):

    import sqlite3

    conn=sqlite3.connect("library.db")

    cursor=conn.cursor()

    cursor.execute(

        "SELECT * FROM books WHERE isbn=?",

        (isbn,)

    )

    data=cursor.fetchall()

    conn.close()

    return data

create_reservation_table()
create_member_table()
create_transaction_table()