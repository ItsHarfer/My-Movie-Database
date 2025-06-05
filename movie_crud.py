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

import movie_storage
import movie_storage_sql
from config import COLOR_ERROR, COLOR_SUCCESS
from printers import print_colored_output


def add_movie(
    new_movie_title: str,
    attributes: dict[str, float | int],
    movie_dict: dict[str, dict[str, float | int]],
) -> None:
    """
    Adds a new movie with arbitrary numeric attributes to the movie dictionary.

    :param movie_dict:
    :param new_movie_title: The title of the movie to be added.
    :param attributes: Dictionary of attributes to assign (e.g. {"rating": 8.5, "release": 1994}).
    :return: None
    """
    if new_movie_title in movie_dict:
        return print_colored_output(
            "❌ Movie is already in the database. Try again.", COLOR_ERROR
        )
    else:
        movie_dict[new_movie_title] = attributes
        movie_storage.add_movie(new_movie_title, attributes)
        return print_colored_output(
            f'✅ "{new_movie_title}" successfully added.',
            COLOR_SUCCESS,
        )


def delete_movie(
    movie_to_delete: str, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Deletes a movie from the database if it exists and provides feedback to the user.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :param movie_to_delete: The title of the movie to delete.
    :return: None
    """
    if movie_to_delete not in movie_dict:
        return print_colored_output(
            f"❌ {movie_to_delete} is not in the database. Try again.", COLOR_ERROR
        )
    else:
        try:
            del movie_dict[movie_to_delete]
            # movie_storage.delete_movie(movie_to_delete)
            movie_storage_sql.delete_movie(movie_to_delete)
            return print_colored_output(
                f'🗑️ "{movie_to_delete}" successfully deleted from the database.',
                COLOR_SUCCESS,
            )
        except KeyError as error:
            return print_colored_output(
                f"❌ Unexpected error: {movie_to_delete} not found in dictionary. "
                f"Error: {error}",
                COLOR_ERROR,
            )


def update_movie(
    movie_name: str, new_rating: float, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Updates a specific attribute (e.g. rating, release) of a movie in the database.

    :param movie_dict:
    :param new_rating:
    :param movie_name: The title of the movie to update.
    :return: None
    """

    if movie_name not in movie_dict:
        return print_colored_output("❌ Movie not found in the database.", COLOR_ERROR)
    else:
        try:
            movie_dict[movie_name]["rating"] = new_rating
            movie_storage.update_movie(movie_name, "rating", new_rating)
            return print_colored_output(f'✅ "{movie_name}" updated!', COLOR_SUCCESS)
        except KeyError as error:
            return print_colored_output(
                f"❌ Unexpected error: {movie_name} not found in dictionary. "
                f"Error: {error}",
                COLOR_ERROR,
            )
