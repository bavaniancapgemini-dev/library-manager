import tkinter as tk
from tkinter import ttk
from add_book_gui import AddBookGUI
from edit_book_gui import EditBookGUI
from database import view_books


class BooksGUI:

    def __init__(self):

        self.window = tk.Toplevel()

        self.window.title("Books Management")

        self.window.geometry("1000x600")

        self.create_widgets()

        self.load_books()

    def create_widgets(self):

        top = tk.Frame(self.window)

        top.pack(fill="x", pady=10)

        tk.Label(

            top,

            text="Search"

        ).pack(side="left", padx=5)

        self.search = tk.Entry(

            top,

            width=40

        )

        self.search.pack(side="left")

        tk.Button(

            top,

            text="Search"

        ).pack(side="left", padx=10)

        columns = (

            "ID",

            "Title",

            "Author",

            "ISBN",

            "Category",

            "Status",

            "Copies"

        )

        self.tree = ttk.Treeview(

            self.window,

            columns=columns,

            show="headings"

        )

        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(col, width=120)

        self.tree.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        bottom = tk.Frame(self.window)

        bottom.pack(pady=10)

        tk.Button(
            bottom,
            text="Add Book",
            width=15,
            command=lambda: AddBookGUI(self.load_books)
        ).grid(row=0,column=0,padx=5)

        tk.Button(
            bottom,
            text="Edit Book",
            width=15,
            command=self.edit_selected
        ).grid(row=0,column=1,padx=5)
        
        tk.Button(

            bottom,

            text="Delete Book",

            width=15

        ).grid(row=0,column=2,padx=5)

        tk.Button(

            bottom,

            text="Refresh",

            width=15,

            command=self.load_books

        ).grid(row=0,column=3,padx=5)

    def load_books(self):

        for row in self.tree.get_children():

            self.tree.delete(row)

        books = view_books()

        for book in books:

            self.tree.insert(

                "",

                "end",

                values=(

                    book[0],

                    book[1],

                    book[2],

                    book[3],

                    book[4],

                    book[5],

                    book[9]

                )

            )
            
    def edit_selected(self):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        books = view_books()

        for book in books:

            if book[0] == values[0]:

                EditBookGUI(
                    book,
                    self.load_books
                )

            break