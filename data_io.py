"""
data_io.py


"""

import json
from typing import Any

# TODO: Edit to the new file system
def get_data_from_file(filename: str) -> list[dict]:
    """
    Load and return ship data from a JSON file.

    :param filename: The path to the JSON file.
    :type filename: str
    :return: A list of ship data dictionaries extracted from the "data" key.
    :rtype: list[dict]
    """
    with open(filename, "r") as file:
        all_data = json.load(file)
    return all_data["data"]


def get_data(raw_data: Any, category: Any, unique: bool = False) -> list | set:
    """
    Extract data from a list of dicts for a given category.

    Entries that do not contain the specified key (category) are skipped.
    A warning is printed indicating how many entries were skipped due to the missing key.

    :param raw_data: List of dictionaries containing ship data.
    :param category: The key to extract from each dictionary.
    :param unique: Whether to return unique values as a set.
    :return: Set of unique values or list of values from the specified category.
    Entries missing the key are skipped.
    """
    values = (item[category] for item in raw_data if category in item)
    result = set(values) if unique else list(values)
    return result


def get_validated_input(prompt: str) -> list[str] | None:
    """
    Prompt the user for input, validate the command and parameters,
    and return the split input as a list.

    :param prompt: The prompt string shown to the user.
    :type prompt: str
    :return: A list containing the command and parameters as strings,
             or None if input is invalid.
    :rtype: list[str] | None
    """
    while True:
        user_input: str = input(prompt).strip()

        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        split_input = user_input.split(" ")
        command, *params = split_input

        from handlers import MOVIE_COMMAND_DISPATCHER

        if not command in MOVIE_COMMAND_DISPATCHER:
            print(f"'{command}' is not a recognized command. Try again.")
            continue

        requires_param = " " in MOVIE_COMMAND_DISPATCHER[command]["label"]
        if requires_param and not params:
            print(f"The '{command}' command requires a param. Try again.")
            continue

        if command == "top_countries" and (not params or not params[0].isnumeric()):
            print("The parameter for 'top_countries' must be a positive number.")
            continue

        return split_input
