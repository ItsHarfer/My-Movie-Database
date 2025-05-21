"""
handlers.py

"""

import sys
from typing import Any

from helpers import (
    quit_application,
    search_movie,
    get_movies_sorted_by_rating,
    get_rating_histogram,
)
from movie_crud import (
    add_movie_to_database,
    delete_movie_from_database,
    update_movie_in_database,
    get_random_movie,
)
from printers import (
    print_movies_in_database,
    print_movies_statistics_in_database,
    print_movies,
)


def handle_quit_application(_, __):
    """
    Quit the application after the user selects this option.

    :param _: Unused parameter (e.g., command-line arguments).
    :param __: Unused second parameter.
    :return: None. Prints the list of commands to the console.
    :rtype: None
    """
    quit_application()


def handle_show_movies(_: Any, movies_data) -> None:
    """
    Display a list of all unique countries represented by ships in the dataset.

    :param _:
    :param movies_data:
    :return: None. Prints a sorted list of unique ship countries.
    :rtype: None
    """
    print_movies_in_database(movies_data)


def handle_add_movie(_, movies_data):
    add_movie_to_database(movies_data)


def handle_delete_movie(_, movie_data):
    delete_movie_from_database(movie_data)


def handle_update_movie(_, movie_data):
    update_movie_in_database(movie_data)


def handle_show_movie_statistics(_, movie_data):
    print_movies_statistics_in_database(movie_data)


def handle_random_movie(_, movie_data):
    random_movie = get_random_movie(movie_data)
    print_movies(random_movie)


def handle_search_movie(_, movie_data):
    search_movie(movie_data)


def handle_sorted_movies_by_rating(_, movie_data):
    print_movies(get_movies_sorted_by_rating(movie_data))


def handle_rating_histogram(_, movie_data):
    get_rating_histogram(movie_data)


# Dispatcher mapping for movie operations
MOVIE_COMMAND_DISPATCHER = {
    0: {
        "handler": handle_quit_application,
        "label": "Quit application",
        "description": "Quit the application.",
    },
    1: {
        "handler": handle_show_movies,
        "label": "List movies",
        "description": "Displays all movies in the database",
    },
    2: {
        "handler": handle_add_movie,
        "label": "Add movie",
        "description": "Adds a new movie to the database",
    },
    3: {
        "handler": handle_delete_movie,
        "label": "Delete movie",
        "description": "Deletes a movie from the database",
    },
    4: {
        "handler": handle_update_movie,
        "label": "Update movie",
        "description": "Updates the rating of an existing movie",
    },
    5: {
        "handler": handle_show_movie_statistics,
        "label": "Stats",
        "description": "Displays statistical information about movies",
    },
    6: {
        "handler": handle_random_movie,
        "label": "Random movie",
        "description": "Selects and shows a random movie",
    },
    7: {
        "handler": handle_search_movie,
        "label": "Search movie",
        "description": "Searches movies by name",
    },
    8: {
        "handler": handle_sorted_movies_by_rating,
        "label": "Movies sorted by rating",
        "description": "Shows movies sorted by rating",
    },
    9: {
        "handler": handle_rating_histogram,
        "label": "Create Rating Histogram",
        "description": "Generates and saves a rating histogram",
    },
}
