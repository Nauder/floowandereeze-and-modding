import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw

# STATIC FUNCTIONS #


MESSAGE_DURATION = 3850


def show_message(title: str, message: str) -> None:
    """Displays a message on a timed popup"""

    top = tk.Toplevel(bg="#1B2838")
    top.title(title)
    frame = tk.Frame(top, width=300, height=200, bg="#1B2838")
    frame.pack()

    pb = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=350, mode="indeterminate")
    pb.pack(expand=True)
    tk.Label(
        frame,
        text=message,
        padx=10,
        pady=20,
        bg="#1B2838",
        fg="#FFF",
        font=("Helvetica", 14),
    ).pack()

    pb.start(32)

    top.after(MESSAGE_DURATION, top.destroy)


def show_error(title: str, message: str) -> None:
    """Displays an error message"""

    top = tk.Toplevel(bg="#9B2838")
    top.title(title)
    frame = tk.Frame(top, width=300, height=300, bg="#9B2838", pady=10)
    frame.pack()

    tk.Label(frame, image="::tk::icons::error").pack()

    tk.Label(
        frame, text="ERROR:", bg="#9B2838", fg="#FFF", font=("Helvetica", 14)
    ).pack()

    tk.Label(
        frame,
        text=message,
        padx=10,
        pady=20,
        bg="#9B2838",
        fg="#FFF",
        font=("Helvetica", 14),
    ).pack()

    tk.Button(
        frame,
        text="Close",
        bg="#333",
        command=lambda: top.destroy(),
        fg="#FFF",
        font=("Helvetica", 14),
        border=0,
        relief=None,
        cursor="hand2",
    ).pack()
