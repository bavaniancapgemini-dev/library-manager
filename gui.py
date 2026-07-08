from tkinter import messagebox
from database import add_book, view_books, update_book, delete_book_by_id, search_books, search_author, search_category, available_books, borrowed_books, dashboard_data
from database import overdue_books, calculate_fine
from datetime import datetime
from reports import export_books
from reports import export_members
from theme import *
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.configure(bg=BG_COLOR)

root.title("Library Manager v8.0")

root.geometry("700x500")

def update_clock():

    now = datetime.now()

    clock.config(

        text=now.strftime(

            "%d-%m-%Y   %I:%M:%S %p"

        )

    )

    root.after(

        1000,

        update_clock

    )

def export_books_gui():

    export_books()

    messagebox.showinfo(

        "Success",

        "Books Report Saved"

    )
    
def export_members_gui():

    export_members()

    messagebox.showinfo(

        "Success",

        "Members Report Saved"

    )

def overdue_window():

    books = overdue_books()

    message = ""

    for book in books:

        fine = calculate_fine(book[7])

        message += f"{book[1]} - ₹{fine}\n"

    if message == "":
        message = "No overdue books."

    messagebox.showinfo(
        "Overdue Books",
        message
    )

def dashboard_window():

    window = tk.Toplevel(root)

    window.title("Library Dashboard")

    window.geometry("450x350")

    books, members, available, borrowed = dashboard_data()

    tk.Label(
        window,
        text="LIBRARY DASHBOARD",
        font=("Arial",18,"bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text=f"📚 Total Books : {books}",
        font=("Arial",14)
    ).pack(pady=10)

    tk.Label(
        window,
        text=f"👥 Total Members : {members}",
        font=("Arial",14)
    ).pack(pady=10)

    tk.Label(
        window,
        text=f"✅ Available Books : {available}",
        font=("Arial",14)
    ).pack(pady=10)

    tk.Label(
        window,
        text=f"📖 Borrowed Books : {borrowed}",
        font=("Arial",14)
    ).pack(pady=10)

def search_window():

    window = tk.Toplevel(root)

    window.title("Search Books")

    window.geometry("400x250")

    tk.Label(

        window,

        text="Book Title"

    ).pack()

    entry = tk.Entry(window,width=30)

    entry.pack()

    def search():

        books = search_books(entry.get())

        message = ""

        for book in books:

            message += str(book) + "\n"

        if message == "":

            message = "No Books Found"

        messagebox.showinfo(

            "Results",

            message

        )

    tk.Button(

        window,

        text="Search",

        command=search

    ).pack(pady=20)

def delete_book_window():

    window = tk.Toplevel(root)

    window.title("Delete Book")

    window.geometry("300x180")

    tk.Label(

        window,

        text="Book ID"

    ).pack(pady=10)

    id_entry = tk.Entry(window)

    id_entry.pack()

    def delete():

        answer = messagebox.askyesno(

            "Confirm",

            "Delete this book?"

        )

        if answer:

            delete_book_by_id(

                int(id_entry.get())

            )

            messagebox.showinfo(

                "Success",

                "Book Deleted"

            )

            window.destroy()

    tk.Button(

        window,

        text="Delete",

        command=delete,

        width=20

    ).pack(pady=20)

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

    font=("Arial",24,"bold"),

    bg=BG_COLOR,

    fg=HEADER_COLOR

)

heading.pack(pady=20)

clock = tk.Label(

    root,

    bg=BG_COLOR,

    font=("Arial",12)

)

clock.pack(pady=5)

welcome = tk.Label(

    root,

    text="Welcome to Library Manager",

    bg=BG_COLOR,

    fg="green",

    font=("Arial",12,"italic")

)

welcome.pack(pady=5)

card = tk.Frame(

    root,

    bg=CARD_COLOR,

    bd=2,

    relief="ridge"

)

card.pack(

    pady=15,

    padx=15,

    fill="x"

)

tk.Label(

    card,

    text="📚 Library Dashboard",

    bg=CARD_COLOR,

    font=("Arial",14,"bold")

).pack(pady=10)


add_btn = tk.Button(

    root,

    text="Add Book",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=add_book_window

)

add_btn.pack(pady=5)

view_btn = tk.Button(

    root,

    text="View Books",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=view_books_window

)

edit_btn = tk.Button(

    root,

    text="Edit Book",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=edit_book_window

)

edit_btn.pack(pady=5)

view_btn.pack(pady=5)

search_btn = tk.Button(

    root,

    text="Search Books",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=search_window

)

search_btn.pack(pady=5)

delete_btn = tk.Button(

    root,

    text="Delete Book",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=delete_book_window

)

delete_btn.pack(pady=5)

dashboard_btn = tk.Button(

    root,

    text="Dashboard",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=dashboard_window

)

dashboard_btn.pack(pady=5)

overdue_btn = tk.Button(

    root,

    text="Overdue Books",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=overdue_window

)

overdue_btn.pack(pady=5)

books_report_btn = tk.Button(

    root,

    text="Export Books Excel",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=export_books_gui

)

books_report_btn.pack(pady=5)

members_report_btn = tk.Button(

    root,

    text="Export Members Excel",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=export_members_gui

)

members_report_btn.pack(pady=5)

exit_btn = tk.Button(

    root,

    text="Exit",

    width=25,
    
    bg=BUTTON_COLOR,

    fg=BUTTON_TEXT,

    font=("Arial",11,"bold"),

    command=root.destroy

)

exit_btn.pack(pady=5)

status = tk.Label(

    root,

    text="Ready",

    bd=1,

    relief=tk.SUNKEN,

    anchor="w"

)

status.pack(

    side="bottom",

    fill="x"

)

update_clock()
root.mainloop()