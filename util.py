import tkinter as tk
from tkinter import ttk

from unicodedata import normalize
from PIL import Image, ImageChops, ImageOps
from re import sub

# STATIC FUNCTIONS #


MESSAGE_DURATION = 3850


def add_sleeve_border(image: Image.Image) -> Image.Image:
    """Adds solid color borders to given image"""

    return ImageOps.expand(
        image, border=(int(image.width * 0.06), int(image.height * 0.05)), fill="black"
    )


def trim(im) -> Image.Image:
    """Removes empty space from the image provided"""

    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def slugify(value, allow_unicode=False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """

    value = str(value)
    if allow_unicode:
        value = normalize("NFKC", value)
    else:
        value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = sub(r"[^\w\s-]", "", value.lower())
    return sub(r"[-\s]+", "-", value).strip("-_")


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


def convert_image(path: str, size: tuple) -> Image.Image:
    """Converts the user given image to its proper size using lanczos resampling"""

    return Image.open(path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
