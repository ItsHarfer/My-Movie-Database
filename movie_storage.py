import json

from config import DATA_FILE, COLOR_ERROR, COLOR_SUCCESS
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
            all_data = json.load(file)
        return dict(all_data)
    except IOError as error:
        print_colored_output(f"❌ Error loading movies from file: {error}", COLOR_ERROR)
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


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movie_list(DATA_FILE)
    del movies[title]
    save_movies(movies, DATA_FILE)


def update_movie(title, attribute, new_value):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movie_list(DATA_FILE)
    movies[title][attribute] = new_value
    save_movies(movies, DATA_FILE)
