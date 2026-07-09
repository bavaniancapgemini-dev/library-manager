import tkinter as tk

from cover_manager import upload_cover

root = tk.Tk()

root.withdraw()

path = upload_cover()

print(path)