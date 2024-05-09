from unicodedata import normalize
from PIL import Image, ImageChops, ImageOps
from re import sub


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


def resize_image(path: str, size: tuple[int, int]) -> Image.Image:
    """Converts the user given image to its proper size using lanczos resampling"""

    return Image.open(path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)


def convert_image(path: str, size: tuple) -> Image.Image:
    """Converts the user given image to its proper size using lanczos resampling"""

    return change_image_ratio(Image.open(path).convert("RGBA"), size)


def change_image_ratio(img: Image, new_ratio: tuple):
    width, height = img.size
    original_ratio = width / height
    new_ratio_value = new_ratio[0] / new_ratio[1]

    if original_ratio > new_ratio_value:
        # If the original ratio is greater than target ratio, then reduce width
        new_width = int(height * new_ratio_value)
        left_margin = (width - new_width) / 2
        img = img.crop((left_margin, 0, width - left_margin, height))
    elif original_ratio < new_ratio_value:
        # If the original ratio is less than target ratio, then reduce height
        new_height = int(width / new_ratio_value)
        top_margin = (height - new_height) / 2
        img = img.crop((0, top_margin, width, height - top_margin))

    return img
