from json import load
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent
PROJECT_UI = f'{PROJECT_PATH}/res/Main.ui'
MESSAGE = {
    "REPLACEMENT": "Asset Replacement",
    "EXTRACTION": "Asset Extraction",
    "SWAPPING": "Asset Swapping",
    "COPYING": "Bundle Copy",
}
FILE = {
    "IMAGE": ["*.png", "*.jpg", "*.jpeg"],
    "IMAGE_NAME": "image.png",
    "UNITY": "data.unity3d",
}
BUTTON = ["<Button-1>", "<Button-3>"]
DATA = load(open(f'{PROJECT_PATH}/data.json', "r+", encoding="cp949"))
FIELD_FLIP_INDEX = 9
