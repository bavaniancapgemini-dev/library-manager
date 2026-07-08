from tkinter import messagebox
from database import add_book, view_books, update_book

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("Library Manager v8.0")

root.geometry("700x500")

def edit_book_window():

    books = view_books()

    if len(books) == 0:

        messagebox.showinfo(

            "Info",

            "No books available."

        )

        return

    window = tk.Toplevel(root)

    window.title("Edit Book")

    window.geometry("400x420")

    tk.Label(window, text="Book ID").pack()

    id_entry = tk.Entry(window)

    id_entry.pack()

    tk.Label(window, text="Title").pack()

    title_entry = tk.Entry(window)

    title_entry.pack()

    tk.Label(window, text="Author").pack()

    author_entry = tk.Entry(window)

    author_entry.pack()

    tk.Label(window, text="Category").pack()

    category_entry = tk.Entry(window)

    category_entry.pack()

    tk.Label(window, text="Copies").pack()

    copies_entry = tk.Entry(window)

    copies_entry.pack()

    def save_changes():

        update_book(

            int(id_entry.get()),

            title_entry.get(),

            author_entry.get(),

            category_entry.get(),

            int(copies_entry.get())

        )

        messagebox.showinfo(

            "Success",

            "Book Updated Successfully"

        )

        window.destroy()

    tk.Button(

        window,

        text="Update Book",

        command=save_changes

    ).pack(pady=15)

def add_book_window():

    window = tk.Toplevel(root)

    window.title("Add Book")

    window.geometry("400x350")

    tk.Label(window, text="Book Title").pack()

    title_entry = tk.Entry(window, width=35)

    title_entry.pack()

    tk.Label(window, text="Author").pack()

    author_entry = tk.Entry(window, width=35)

    author_entry.pack()

    tk.Label(window, text="Category").pack()

    category_entry = tk.Entry(window, width=35)

    category_entry.pack()

    tk.Label(window, text="Copies").pack()

    copies_entry = tk.Entry(window, width=35)

    copies_entry.pack()

    def save():

        title = title_entry.get()

        author = author_entry.get()

        category = category_entry.get()

        copies = copies_entry.get()

        if title == "" or author == "" or category == "" or copies == "":

            messagebox.showerror(

                "Error",

                "Please fill all fields."

            )

            return

        add_book(

            title,

            author,

            category,

            int(copies)

        )

        messagebox.showinfo(

            "Success",

            "Book Added Successfully!"

        )

        window.destroy()

    tk.Button(

        window,

        text="Save Book",

        command=save,

        width=20

    ).pack(pady=15)
    
def view_books_window():

    window = tk.Toplevel(root)

    window.title("Library Books")

    window.geometry("900x400")

    columns = (

        "ID",

        "Title",

        "Author",

        "Category",

        "Status",

        "Copies"

    )

    tree = ttk.Treeview(

        window,

        columns=columns,

        show="headings"

    )

    for col in columns:

        tree.heading(col, text=col)

        tree.column(col, width=130)

    tree.pack(

        fill="both",

        expand=True

    )

    books = view_books()

    for book in books:

        tree.insert(

            "",

            tk.END,

            values=book

        )

heading = tk.Label(

    root,

    text="LIBRARY MANAGER",

    font=("Arial",22,"bold")

)

heading.pack(pady=20)

add_btn = tk.Button(

    root,

    text="Add Book",

    width=25,

    command=add_book_window

)

add_btn.pack(pady=5)

view_btn = tk.Button(

    root,

    text="View Books",

    width=25,

    command=view_books_window

)

edit_btn = tk.Button(

    root,

    text="Edit Book",

    width=25,

    command=edit_book_window

)

edit_btn.pack(pady=5)

view_btn.pack(pady=5)

search_btn = tk.Button(

    root,

    text="Search Book",

    width=25

)

search_btn.pack(pady=5)

delete_btn = tk.Button(

    root,

    text="Delete Book",

    width=25

)

delete_btn.pack(pady=5)

exit_btn = tk.Button(

    root,

    text="Exit",

    width=25,

    command=root.destroy

)

exit_btn.pack(pady=5)



root.mainloop()