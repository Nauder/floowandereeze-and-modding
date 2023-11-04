from json import dump

from util.constants import DATA, PROJECT_PATH


def update_json() -> None:
    """Updates the data json with the session's data"""

    with open(f'{PROJECT_PATH}/data.json', "w") as f:
        dump(DATA, f)
