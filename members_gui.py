import tkinter as tk
from database import view_members


class MembersGUI:

    def __init__(self):

        window = tk.Toplevel()

        window.title("Members")

        members = view_members()

        text = tk.Text(

            window,

            width=70,

            height=20

        )

        text.pack()

        for member in members:

            text.insert(

                tk.END,

                str(member)+"\n"

            )