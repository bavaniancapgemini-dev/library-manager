import tkinter as tk
from tkinter import messagebox
from database import add_book


class AddBookGUI:

    def __init__(self, refresh_callback=None):

        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel()

        self.window.title("Add New Book")

        self.window.geometry("400x420")

        tk.Label(self.window, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self.window, width=40)
        self.title_entry.pack()

        tk.Label(self.window, text="Author").pack(pady=5)
        self.author_entry = tk.Entry(self.window, width=40)
        self.author_entry.pack()

        tk.Label(self.window, text="ISBN").pack(pady=5)
        self.isbn_entry = tk.Entry(self.window, width=40)
        self.isbn_entry.pack()

        tk.Label(self.window, text="Category").pack(pady=5)
        self.category_entry = tk.Entry(self.window, width=40)
        self.category_entry.pack()

        tk.Label(self.window, text="Copies").pack(pady=5)
        self.copies_entry = tk.Entry(self.window, width=40)
        self.copies_entry.pack()

        tk.Button(
            self.window,
            text="Save Book",
            command=self.save_book,
            width=20
        ).pack(pady=20)

    def save_book(self):

        try:

            add_book(
                self.title_entry.get(),
                self.author_entry.get(),
                self.isbn_entry.get(),
                self.category_entry.get(),
                int(self.copies_entry.get())
            )

            messagebox.showinfo(
                "Success",
                "Book Added Successfully"
            )

            if self.refresh_callback:
                self.refresh_callback()

            self.window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )