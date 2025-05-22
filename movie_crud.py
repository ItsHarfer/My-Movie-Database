"""
movie_crud.py

Provides core CRUD (Create, Read, Update, Delete) operations for managing movies in the database.

This module contains functions to:
- Add new movies with flexible attributes
- Delete existing movies
- Update specific attributes of a movie

Each function works directly on the in-memory movie dictionary and provides immediate
user feedback through colored console output. The module focuses on modifying the
movie dataset based on user actions, and complements the higher-level handler logic.

Used primarily by menu handler functions in the application.
"""

from printers import print_colored_output


def add_movie(
    movie_dict: dict[str, dict[str, float | int]],
    new_movie_name: str,
    attributes: dict[str, float | int],
) -> None:
    """
    Adds a new movie with arbitrary numeric attributes to the movie dictionary.

    :param movie_dict: Dictionary of movies with their attributes.
    :param new_movie_name: The title of the movie to be added.
    :param attributes: Dictionary of attributes to assign (e.g. {"rating": 8.5, "release": 1994}).
    :return: None
    """
    if new_movie_name not in movie_dict:
        movie_dict[new_movie_name] = attributes
        info_string = ", ".join(f"{key}: {value}" for key, value in attributes.items())
        print_colored_output(
            f'✅ "{new_movie_name}" successfully added with attributes ({info_string}).',
            "green",
        )
    else:
        print_colored_output("❌ Movie is already in the database. Try again.", "red")


def delete_movie(
    movie_dict: dict[str, dict[str, float | int]], movie_to_delete: str
) -> None:
    """
    Deletes a movie from the database if it exists and provides feedback to the user.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :param movie_to_delete: The title of the movie to delete.
    :return: None
    """
    movie_is_in_database = movie_to_delete in movie_dict

    if movie_is_in_database:
        del movie_dict[movie_to_delete]
        print_colored_output(
            f'🗑️ "{movie_to_delete}" successfully deleted from the database.', "green"
        )
    else:
        print_colored_output("Movie is not in the database. Try again.", "red")


def update_movie(
    movie_dict: dict[str, dict[str, float | int]],
    movie_name: str,
    attribute: str,
    new_value: float | int,
) -> None:
    """
    Updates a specific attribute (e.g. rating, release) of a movie in the database.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :param movie_name: The title of the movie to update.
    :param attribute: The attribute key to update (e.g. "rating").
    :param new_value: The new value to assign to the specified attribute.
    :return: None
    """
    if movie_name in movie_dict:
        if attribute in movie_dict[movie_name]:
            movie_dict[movie_name][attribute] = new_value
            print_colored_output(f'✅ "{movie_name}" {attribute} updated!', "green")
        else:
            print_colored_output(
                f'❌ Attribute "{attribute}" not found for movie "{movie_name}".', "red"
            )
    else:
        print_colored_output("❌ Movie not found in the database.", "red")
