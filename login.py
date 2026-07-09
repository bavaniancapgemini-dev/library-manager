import tkinter as tk
from tkinter import messagebox
from auth import login


class LoginWindow:

    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Library Login")

        self.window.geometry("350x250")

        tk.Label(
            self.window,
            text="Username"
        ).pack(pady=5)

        self.username = tk.Entry(self.window)

        self.username.pack()

        tk.Label(
            self.window,
            text="Password"
        ).pack(pady=5)

        self.password = tk.Entry(
            self.window,
            show="*"
        )

        self.password.pack()

        tk.Button(
            self.window,
            text="Login",
            command=self.check_login
        ).pack(pady=20)

        self.window.mainloop()

    def check_login(self):

        user = login(

            self.username.get(),

            self.password.get()

        )

        if user:

            self.window.destroy()

            from dashboard import Dashboard

            Dashboard(user[0])

        else:

            messagebox.showerror(

                "Error",

                "Invalid Username or Password"

            )