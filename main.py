from database import (
    add_book,
    view_books,
    delete_book
)

from search import search_book
from reports import total_books
from utils import title


while True:

    title()

    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Delete Book")
    print("5. Total Books")
    print("6. Exit")

    choice = input("Choose: ")


    if choice == "1":

        title_name = input("Book Title: ")

        author = input("Author: ")

        add_book(title_name, author)

        print("Book Added")


    elif choice == "2":

        books = view_books()

        for book in books:

            print(book)


    elif choice == "3":

        keyword = input("Search title: ")

        results = search_book(keyword)

        for item in results:

            print(item)


    elif choice == "4":

        title_name = input("Enter title to delete: ")

        delete_book(title_name)

        print("Book Deleted")


    elif choice == "5":

        print("Total Books:", total_books())


    elif choice == "6":

        break


    else:

        print("Invalid Choice")