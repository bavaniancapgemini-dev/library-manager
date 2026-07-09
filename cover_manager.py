import os
import shutil
from tkinter import filedialog


def upload_cover():

    project_folder = os.path.dirname(os.path.abspath(__file__))

    covers_folder = os.path.join(project_folder, "Covers")

    os.makedirs(covers_folder, exist_ok=True)

    file = filedialog.askopenfilename(
        title="Select Book Cover",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if not file:
        return ""

    filename = os.path.basename(file)

    destination = os.path.join(covers_folder, filename)

    shutil.copy2(file, destination)

    return destination