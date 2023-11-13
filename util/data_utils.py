from json import dump

from util.constants import DATA, PROJECT_PATH


def update_json() -> None:
    """Updates the data json with the session's data"""

    with open(f'{PROJECT_PATH}/data.json', "w") as f:
        dump(DATA, f)


def reset_data() -> None:
    DATA["gamePath"] = "empty"
    DATA["lastImage"] = "empty"
    DATA["lastArt"] = "empty"
    DATA["lastField"] = "empty"
    DATA["lastIcon"] = "empty"
    DATA["lastSleeveDx"] = "empty"
    DATA["lastHome"] = "empty"
    DATA["lastFace"] = "empty"
    DATA["background"] = "empty"
    DATA["lastWallpaper"] = [
        "empty",
        "empty"
    ]

    update_json()
