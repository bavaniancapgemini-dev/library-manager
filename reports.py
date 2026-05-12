from database import view_books


def total_books():

    books = view_books()

    return len(books)