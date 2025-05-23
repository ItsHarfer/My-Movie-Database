"""
data_io.py


"""

import json


def get_data_from_file(filename: str) -> dict[str, dict[str, float | int]]:
    """
    Loads and returns structured movie (or ship) data from a JSON file.

    Expects the file to contain a dictionary of string keys mapping to dictionaries
    with numeric attributes like ratings or release years.

    :param filename: Path to the JSON file to be loaded.
    :return: Dictionary of items, each containing attribute dictionaries with float or int values.
    """
    with open(filename, "r") as file:
        all_data = json.load(file)
    return all_data
