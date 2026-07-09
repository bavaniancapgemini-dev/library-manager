import tkinter as tk
from tkinter import messagebox
from database import update_book


class EditBookGUI:

    def __init__(self, book, refresh_callback=None):

        self.book = book
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel()

        self.window.title("Edit Book")

        self.window.geometry("400x420")

        tk.Label(self.window, text="Title").pack(pady=5)
        self.title = tk.Entry(self.window, width=40)
        self.title.pack()
        self.title.insert(0, book[1])

        tk.Label(self.window, text="Author").pack(pady=5)
        self.author = tk.Entry(self.window, width=40)
        self.author.pack()
        self.author.insert(0, book[2])

        tk.Label(self.window, text="ISBN").pack(pady=5)
        self.isbn = tk.Entry(self.window, width=40)
        self.isbn.pack()
        self.isbn.insert(0, book[3])

        tk.Label(self.window, text="Category").pack(pady=5)
        self.category = tk.Entry(self.window, width=40)
        self.category.pack()
        self.category.insert(0, book[4])

        tk.Label(self.window, text="Copies").pack(pady=5)
        self.copies = tk.Entry(self.window, width=40)
        self.copies.pack()
        self.copies.insert(0, book[9])

        tk.Button(
            self.window,
            text="Update Book",
            command=self.update
        ).pack(pady=20)

    def update(self):

        try:

            update_book(

                self.book[0],

                self.title.get(),

                self.author.get(),

                self.isbn.get(),

                self.category.get(),

                int(self.copies.get())

            )

            messagebox.showinfo(
                "Success",
                "Book Updated Successfully"
            )

            if self.refresh_callback:

                self.refresh_callback()

            self.window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e))