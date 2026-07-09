import tkinter as tk


class Dashboard:

    def __init__(self, role):

        self.root = tk.Tk()

        self.root.title("Library Dashboard")

        self.root.geometry("700x500")

        tk.Label(

            self.root,

            text=f"Welcome {role}",

            font=("Arial",20)

        ).pack(pady=20)

        tk.Button(

            self.root,

            text="Books",

            width=25,

            height=2,

            command=self.books

        ).pack(pady=10)

        tk.Button(

            self.root,

            text="Members",

            width=25,

            height=2,

            command=self.members

        ).pack(pady=10)

        tk.Button(

            self.root,

            text="Exit",

            width=25,

            height=2,

            command=self.root.destroy

        ).pack(pady=10)

        self.root.mainloop()

    def books(self):

        from books_gui import BooksGUI

        BooksGUI()

    def members(self):

        from members_gui import MembersGUI

        MembersGUI()