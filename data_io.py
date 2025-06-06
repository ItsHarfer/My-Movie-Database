"""
file_io.py

Utility module for reading and writing data to files in plain text or JSON format.

Functions:
- load_data: Load file content as plain text or parsed JSON.
- save_data: Write string or JSON content to a file.

These helper functions are used throughout the application to persist and retrieve data.

Author: Martin Haferanke
Date: 06.06.2025
"""

import json


def load_data(file_path: str, is_json: bool = False) -> str | dict:
    """
    Reads data from the specified file path.

    :param file_path: Path to the file to read.
    :param is_json: Whether to parse the file as JSON. Defaults to False.
    :return: Parsed JSON data as a dictionary if is_json is True,
             otherwise the file content as a string.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file) if is_json else file.read()
    except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return "" if not is_json else {}


def save_data(file_path: str, html: str, is_json: bool = False) -> None:
    """
    Saves data to the specified file path.

    :param file_path: Path to the file to save.
    :param html: Content to write to the file.
    :param is_json: Whether to save the content as JSON. Defaults to False.
    :return: None
    """
    try:
        with open(file_path, "w") as file:
            file.write(json.dumps(html)) if is_json else file.write(html)
            return print("HTML saved successfully.")
    except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
        return print(f"Error saving file {file_path}: {e}")
