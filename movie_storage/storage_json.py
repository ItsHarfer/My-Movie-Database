"""
storage_json.py

This module handles low-level JSON-based storage operations for the movie database application.

It provides functions to:
- Load and save movie data to/from a JSON file
- Perform CRUD operations (create, read, update, delete) on individual movie entries
- Validate basic data integrity and catch I/O or format-related errors
- Output meaningful user feedback for failed operations

All data is stored in a dictionary format, with movie titles as keys and
attribute dictionaries (e.g. rating, year) as values.

Author: Martin Haferanke
Date: 13.06.2025
"""

import json

from config.config import DATA_FILE, COLOR_ERROR
from printers import print_colored_output


def get_movie_list(filename: str) -> dict[str, dict[str, float | int]]:
    """
    Loads and returns structured movie (or ship) data from a JSON file.

    Expects the file to contain a dictionary of string keys mapping to dictionaries
    with numeric attributes like ratings or release years.

    :param filename: Path to the JSON file to be loaded.
    :return: Dictionary of items, each containing attribute dictionaries with float or int values.
    """
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            if not content:
                return {}
            json_object = dict(json.loads(content))
            return json_object

    except (IOError, json.JSONDecodeError) as error:
        print_colored_output(
            f"❌ Error loading movies from JSON file: {error}", COLOR_ERROR
        )
        return {}


def save_movies(movie_dict: dict[str, dict[str, float | int]], filename: str) -> None:
    """
    Saves the given movie dictionary to a JSON file.

    Attempts to write the provided dictionary to the specified filename.
    If an I/O error occurs, it prints an error message and returns False.

    :param movie_dict: Dictionary of movies with their attributes.
    :param filename: Path to the JSON file where the data should be saved.
    :return: True if saving was successful, False otherwise.
    """
    try:
        with open(filename, "w") as file:
            json.dump(movie_dict, file, indent=4)
    except IOError as error:
        print_colored_output(f"❌ Error saving movies to file: {error}", COLOR_ERROR)


def add_movie(title: str, attributes: dict[str, float | int]) -> None:
    """
    Adds a new movie with its attributes to the movie database.

    Loads the existing movie data from the JSON file, adds the new movie
    if it doesn't already exist, and saves the updated data back to the file.
    Provides colored console output to indicate success or duplication.

    :param title: The title of the movie to be added.
    :param attributes: Dictionary of numeric attributes (e.g. {"rating": 8.5, "release": 1994}).
    :return: None
    """
    movies = get_movie_list(DATA_FILE)
    movies[title] = attributes
    save_movies(movies, DATA_FILE)


def delete_movie(title: str) -> None:
    """
    Deletes a movie from the movie database.

    Loads the existing movie data from the JSON file, removes the specified movie
    if it exists, and saves the updated data. If the movie is not found,
    an error message is printed.

    :param title: The title of the movie to be deleted.
    :return: None
    """
    movies = get_movie_list(DATA_FILE)
    try:
        del movies[title]
    except KeyError as error:
        return print_colored_output(
            f"❌ Cant delete movie. Error: {error}", COLOR_ERROR
        )

    return save_movies(movies, DATA_FILE)


def update_movie(title: str, attribute: str, new_value: float | int) -> None:
    """
    Updates a specific attribute of a movie in the movies database.

    Loads the existing movie data from the JSON file, updates the specified
    attribute of the given movie, and saves the updated data back to the file.

    :param title: The title of the movie to update.
    :param attribute: The name of the attribute to update (e.g., "rating").
    :param new_value: The new value to assign to the attribute.
    :return: None
    """
    movies = get_movie_list(DATA_FILE)
    try:
        movies[title][attribute] = new_value
    except KeyError as error:
        return print_colored_output(
            f"❌ Cant update movie. Error: {error}", COLOR_ERROR
        )
    return save_movies(movies, DATA_FILE)
