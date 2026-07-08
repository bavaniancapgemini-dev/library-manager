from database import (
    add_book,
    view_books,
    delete_book,
    available_books,
    borrowed_books,
    update_status,
    add_member,
    view_members,
    borrow_book,
    return_book,
    search_member,
    total_members,
    view_transactions,
    overdue_books,
    calculate_fine,
    dashboard,
    most_borrowed,
    export_transactions,
    reserve_book,
    view_reservations,
    restock_book,
    low_stock
)

from search import search_book
from reports import total_books
from utils import title
from auth import login, register

print("===== LIBRARY LOGIN =====")

username = input("Username: ")

password = input("Password: ")

user = login(username, password)

if not user:

    print("Invalid Login")

    exit()

role = user[0]

print("Welcome", role)


while True:

    title()

    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Delete Book")
    print("5. Total Books")
    print("6. View Available Books")
    print("7. View Borrowed Books")
    print("8. Update Book Status")
    print("9. Add Member")
    print("10. View Members")
    print("11. Borrow Book")
    print("12. Return Book")
    print("13. Search Member")
    print("14. Total Members")
    print("15. Borrow History")
    print("16. Overdue Books")
    print("17. Fine Calculator")
    print("18. Library Dashboard")
    print("19. Export Transactions")
    print("20. Reserve Book")
    print("21. View Reservations")
    print("22. Restock Books")
    print("23. Low Stock Report")
    print("24. Add Librarian")
    print("25. Exit")

    choice = input("Choose: ")


    if choice == "1":

        title_name = input("Book Title: ")

        author = input("Author: ")

        category = input("Category: ")

        copies = int(input("Number of Copies: "))

        add_book(

            title,

            author,

            category,

            copies
        )
        print("Book Added Successfully")

        print("Book Added")


    elif choice == "2":

        books = view_books()

        print("\n===== LIBRARY BOOKS =====\n")

        for book in books:

            print("ID      :", book[0])

            print("Title   :", book[1])

            print("Author  :", book[2])

            print("Category:", book[3])

            print("Status  :", book[4])

            print("-"*40)

    elif choice == "3":

        keyword = input("Search title: ")

        results = search_book(keyword)

        for item in results:

            print(item)


    elif choice == "4":

        if role != "Admin":

            print("❌ Only Admin can delete books.")

        else:

            title_name = input("Enter title to delete: ")

            delete_book(title_name)

            print("Book Deleted")

    elif choice == "5":

        print("Total Books:", total_books())

    elif choice == "6":

        books = available_books()

        print("\n===== AVAILABLE BOOKS =====\n")

        for book in books:

            print(book)
            
    elif choice == "7":

        books = borrowed_books()

        print("\n===== BORROWED BOOKS =====\n")

        for book in books:

            print(book)
            
    elif choice == "8":

        title_name = input("Book Title: ")

        print("1. Available")

        print("2. Borrowed")

        option = input("Choose Status: ")

        if option == "1":

            status = "Available"

        else:

            status = "Borrowed"

        update_status(

            title_name,

            status

        )

        print("Status Updated")
        
    elif choice == "9":
        
        if role != "Admin":
            
            print("Only Admin can Delete Books")
            
        else:

            name = input("Member Name: ")

            email = input("Member Email: ")

            add_member(name, email)

            print("Member Added Successfully")
        
    elif choice == "10":

        members = view_members()

        print("\n===== MEMBERS =====\n")

        for member in members:

            print(member)
            
    elif choice == "11":

        title_name = input("Book Title: ")

        from datetime import datetime, timedelta

        member = input("Member Name: ")

        borrow_date = datetime.now().strftime("%Y-%m-%d")

        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        borrow_book(
            title_name,
            member,
            borrow_date,
            due_date
        )

        print("Book Borrowed")

        print("Due Date:", due_date)

        print("Book Borrowed")
        
    elif choice == "12":

        title_name = input("Book Title: ")

        return_book(title_name)

        print("Book Returned")
        
    elif choice == "13":

        keyword = input("Member Name: ")

        data = search_member(keyword)

        for member in data:

            print(member)
            
    elif choice == "14":

        print(

            "Total Members:",

            total_members()

        )
        
    elif choice == "15":
        
        history = view_transactions()
        
        print("\n===== BORROW HISTORY =====\n")
        
        for item in history:
            
            print(item)
            
    elif choice == "16":
        
        books = overdue_books()
        
        print("\n===== OVERDUE BOOKS =====\n")
        
        for book in books:
            
            print(book)
            
    elif choice == "17":

        fines = calculate_fine()

        print("\n===== FINES =====\n")

        for item in fines:

            print(

                "Book:", item[0]

            )

            print(
                "Member:", item[1]

            )

            print(

                "Days:", item[2]

            )

            print(

                "Fine: ₹", item[3]

            )

            print("-"*40)
            
    elif choice == "18":

        stats = dashboard()

        print("\n===== LIBRARY DASHBOARD =====\n")

        print("Total Books :", stats[0])

        print("Available   :", stats[1])

        print("Borrowed    :", stats[2])

        print("Members     :", stats[3])

        print("\nMost Borrowed Books\n")

        for book in most_borrowed():

            print(book)
            
    elif choice == "19":

        export_transactions()

        print("transactions.csv created successfully")
        
    elif choice=="20":
        
        member=input("Member Name: ")
        
        book=input("Book Title: ")
        
        reserve_book(
            
            member,
            book
        )
        print("Book Reserved")
        
    elif choice=="21":

        reservations=view_reservations()

        print("\n===== RESERVATIONS =====\n")

        for item in reservations:

            print(item)
            
    elif choice=="22":
        
        if role != "Admin":
            
            print("❌ Only Admin can delete books.")
            
        else:

            title=input("Book Title: ")

            qty=int(input("Copies To Add: "))

            restock_book(

                title,

                qty

            )

        print("Stock Updated")
        
    elif choice=="23":

        books=low_stock()

        print("\n===== LOW STOCK =====\n")

        for item in books:

            print(item)
            
    elif choice=="24":

        if role != "Admin":

            print("Only Admin Can Add Librarians")

        else:

            username = input("Enter Username: ")

            password = input("Enter Password: ")

            register(

                username,

                password,

                "Librarian"

            )

            print("Librarian Added Successfully")
        
    elif choice == "25":

        break

    else:

        print("Invalid Choice")