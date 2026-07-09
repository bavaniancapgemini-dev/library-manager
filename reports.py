from openpyxl import Workbook
import sqlite3
import os

def export_books():

    if not os.path.exists("Reports"):

        os.mkdir("Reports")

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Books"

    sheet.append(

        [

            "ID",

            "Title",

            "Author",

            "Category",

            "Status",

            "Borrowed By",

            "Borrow Date",

            "Due Date"

        ]

    )

    for book in books:

        sheet.append(book)

    workbook.save(

        "Reports/Books_Report.xlsx"

    )

    conn.close()
    
def export_members():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM members"

    )

    members = cursor.fetchall()

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Members"

    sheet.append(

        [

            "ID",

            "Name",

            "Phone"

        ]

    )

    for member in members:

        sheet.append(member)

    workbook.save(

        "Reports/Members_Report.xlsx"

    )

    conn.close()
    
def total_books():

    conn = sqlite3.connect("library.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM books"

    )

    total = cursor.fetchone()[0]

    conn.close()

    return total