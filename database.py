import sqlite3
from datetime import datetime, timedelta
import csv

DATABASE = "library.db"


def get_connection():
    return sqlite3.connect(DATABASE)

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_name TEXT,
        book_title TEXT,
        reservation_date TEXT
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waitlist(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_title TEXT,
        member_name TEXT,
        request_date TEXT
    )
    """)

    conn.commit()
    conn.close()


initialize_database()

def add_book(title, author, isbn, category, copies):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO books
        (
            title,
            author,
            isbn,
            category,
            status,
            borrowed_by,
            borrow_date,
            due_date,
            copies
        )

        VALUES
        (?,?,?,?,?,?,?,?,?)
        """,

        (
            title,
            author,
            isbn,
            category,
            "Available",
            "",
            "",
            "",
            copies
        )
    )

    conn.commit()
    conn.close()
    
def view_books():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM books

        ORDER BY title

    """)

    books = cursor.fetchall()

    conn.close()

    return books

def delete_book(title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM books WHERE title=?",

        (title,)

    )

    conn.commit()

    conn.close()

def update_book(book_id, title, author, isbn, category, copies):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books

        SET

        title=?,

        author=?,

        isbn=?,

        category=?,

        copies=?

        WHERE id=?
        """,

        (
            title,
            author,
            isbn,
            category,
            copies,
            book_id
        )
    )

    conn.commit()

    conn.close()
    
def available_books():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM books WHERE status='Available'"

    )

    books = cursor.fetchall()

    conn.close()

    return books


def borrowed_books():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM books WHERE status='Borrowed'"

    )

    books = cursor.fetchall()

    conn.close()

    return books

def update_status(title, status):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET status=?
        WHERE title=?
        """,
        (
            status,
            title
        )
    )

    conn.commit()

    conn.close()

def add_member(name, phone):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO members(name,phone) VALUES(?,?)",

        (name, phone)

    )

    conn.commit()

    conn.close()


def view_members():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM members ORDER BY name"

    )

    members = cursor.fetchall()

    conn.close()

    return members


def search_member(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM members WHERE name LIKE ?",

        ("%"+keyword+"%",)

    )

    data = cursor.fetchall()

    conn.close()

    return data


def total_members():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM members"

    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def borrow_book(title, member, borrow_date, due_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status,copies
        FROM books
        WHERE title=?
        """,
        (title,)
    )

    book = cursor.fetchone()

    if book is None:

        conn.close()
        return False

    if book[1] <= 0:

        conn.close()
        return False

    cursor.execute(
        """
        UPDATE books
        SET
            status=?,
            borrowed_by=?,
            borrow_date=?,
            due_date=?,
            copies=copies-1
        WHERE title=?
        """,
        (
            "Borrowed",
            member,
            borrow_date,
            due_date,
            title
        )
    )

    cursor.execute(
        """
        INSERT INTO transactions
        (
            book_title,
            member_name,
            borrow_date,
            due_date,
            return_date
        )
        VALUES(?,?,?,?,?)
        """,
        (
            title,
            member,
            borrow_date,
            due_date,
            ""
        )
    )

    conn.commit()
    conn.close()

    return True

def return_book(title):

    conn = get_connection()

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        UPDATE books
        SET
            status='Available',
            borrowed_by='',
            borrow_date='',
            due_date='',
            copies=copies+1
        WHERE title=?
        """,
        (title,)
    )

    cursor.execute(
        """
        UPDATE transactions
        SET
            return_date=?
        WHERE
            book_title=?
        AND
            return_date=''
        """,
        (
            today,
            title
        )
    )

    conn.commit()

    conn.close()
    
def view_transactions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            book_title,
            member_name,
            borrow_date,
            due_date,
            return_date
        FROM transactions

        ORDER BY borrow_date DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data
    
def overdue_books():

    conn = get_connection()

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT
            book_title,
            member_name,
            due_date
        FROM transactions

        WHERE

        due_date < ?

        AND

        return_date=''
        """,
        (today,)
    )

    books = cursor.fetchall()

    conn.close()

    return books

def calculate_fine():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

        book_title,

        member_name,

        due_date

        FROM transactions

        WHERE return_date=''
        """
    )

    rows = cursor.fetchall()

    conn.close()

    fines = []

    today = datetime.now()

    for row in rows:

        due = datetime.strptime(
            row[2],
            "%Y-%m-%d"
        )

        if today > due:

            days = (today-due).days

            fine = days*10

            fines.append(

                (

                    row[0],

                    row[1],

                    days,

                    fine

                )

            )

    return fines

def dashboard():

    conn = get_connection()

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

    cursor.execute(
        "SELECT SUM(copies) FROM books"
    )

    stock = cursor.fetchone()[0]

    conn.close()

    return (

        total_books,

        available,

        borrowed,

        members,

        stock

    )
    
def most_borrowed():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        book_title,

        COUNT(*) AS total

    FROM transactions

    GROUP BY book_title

    ORDER BY total DESC

    LIMIT 10

    """)

    books = cursor.fetchall()

    conn.close()

    return books

import csv

def export_transactions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM transactions

    ORDER BY borrow_date DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    with open(

        "transactions.csv",

        "w",

        newline="",

        encoding="utf-8"

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
        
def reserve_book(member, book):

    conn = get_connection()

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        INSERT INTO reservations
        (
            member_name,
            book_title,
            reservation_date
        )

        VALUES(?,?,?)
        """,
        (
            member,
            book,
            today
        )
    )

    conn.commit()

    conn.close()
    
def view_reservations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM reservations

        ORDER BY reservation_date DESC
        """
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

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        title,

        author,

        copies

    FROM books

    WHERE copies<=2

    ORDER BY copies ASC

    """)

    books = cursor.fetchall()

    conn.close()

    return books

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

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM books

        WHERE title LIKE ?
        """,
        ("%"+keyword+"%",)
    )

    books = cursor.fetchall()

    conn.close()

    return books

def search_author(author):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM books

        WHERE author LIKE ?
        """,
        ("%"+author+"%",)
    )

    books = cursor.fetchall()

    conn.close()

    return books

def search_category(category):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM books

        WHERE category LIKE ?
        """,
        ("%"+category+"%",)
    )

    books = cursor.fetchall()

    conn.close()

    return books

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

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reviews
        (
            book_title,
            member_name,
            rating,
            review
        )

        VALUES(?,?,?,?)
        """,
        (
            book_title,
            member_name,
            rating,
            review
        )
    )

    conn.commit()

    conn.close()
    
def view_reviews(book_title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

        member_name,

        rating,

        review

        FROM reviews

        WHERE book_title=?

        ORDER BY rating DESC
        """,
        (book_title,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

def search_isbn(isbn):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM books

        WHERE isbn=?
        """,
        (isbn,)
    )

    books = cursor.fetchall()

    conn.close()

    return books

def join_waitlist(book_title, member_name):

    conn = get_connection()

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        INSERT INTO waitlist
        (
            book_title,
            member_name,
            request_date
        )

        VALUES(?,?,?)
        """,
        (
            book_title,
            member_name,
            today
        )
    )

    conn.commit()

    conn.close()
    
def view_waitlist(book_title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

        member_name,

        request_date

        FROM waitlist

        WHERE book_title=?

        ORDER BY id
        """,
        (book_title,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

def next_waiting_member(book_title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

        id,

        member_name

        FROM waitlist

        WHERE book_title=?

        ORDER BY id

        LIMIT 1
        """,
        (book_title,)
    )

    person = cursor.fetchone()

    conn.close()

    return person
    
def remove_from_waitlist(wait_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM waitlist WHERE id=?",
        (wait_id,)
    )

    conn.commit()

    conn.close()
    
def average_rating(book_title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(rating)

        FROM reviews

        WHERE book_title=?
        """,
        (book_title,)
    )

    rating = cursor.fetchone()[0]

    conn.close()

    return rating

def top_rated_books():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        book_title,

        ROUND(AVG(rating),2)

    FROM reviews

    GROUP BY book_title

    ORDER BY AVG(rating) DESC

    LIMIT 10

    """)

    books = cursor.fetchall()

    conn.close()

    return books

def category_statistics():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        category,

        COUNT(*)

    FROM books

    GROUP BY category

    ORDER BY COUNT(*) DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data

def is_book_available(title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT copies

        FROM books

        WHERE title=?

        """,

        (title,)

    )

    result = cursor.fetchone()

    conn.close()

    if result is None:

        return False

    return result[0] > 0

def total_fine_collection():

    fines = calculate_fine()

    total = 0

    for item in fines:

        total += item[3]

    return total

def recent_borrows():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        book_title,

        member_name,

        borrow_date

    FROM transactions

    ORDER BY id DESC

    LIMIT 10

    """)

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