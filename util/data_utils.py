from json import dump

from util.constants import DATA


def update_json() -> None:
    """Updates the data json with the session's data"""

    with open("data.json", "w") as f:
        dump(DATA, f)
