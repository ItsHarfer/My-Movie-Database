"""
handlers.py

This module defines all handler functions for user-interaction in the movie database
application. These functions serve as the interface between user commands (e.g. menu
selections) and the core application logic.

Each handler corresponds to a specific action, such as adding, deleting, updating,
listing, sorting, or analyzing movies. Additionally, this module manages output
presentation and user input handling where appropriate.

The handlers are designed to be used in conjunction with a dispatcher (MOVIE_COMMAND_DISPATCHER)
that maps user commands to the appropriate function.

Main functionalities include:
- Adding, deleting, and updating movies
- Listing all movies or searching/sorting them
- Showing statistics and generating visualizations (e.g. rating histogram)
- Selecting a random movie
- Gracefully exiting the application
"""

import datetime

from analysis import (
    get_calculated_average_rate,
    get_calculated_median_rate,
    get_all_movies_extremes_by_mode,
    get_random_movie,
)
from config import FIRST_FILM_RELEASE, RATING_BASE, RATING_LIMIT, COLOR_ERROR
from helpers import (
    quit_application,
    get_movies_sorted_by_attribute,
    get_colored_input,
    get_colored_numeric_input_float,
    find_movie,
    filter_movies_by_search_query,
    create_histogram_by_attribute,
)
from movie_crud import (
    add_movie,
    delete_movie,
    update_movie,
)
from printers import (
    print_all_movies,
    print_movies_statistics,
    print_movies,
    print_movie,
    print_search_results,
    print_title,
    print_colored_output,
)


def handle_quit_application(_, __):
    """
    Quit the application after the user selects this option.

    :param _: Unused parameter.
    :param __: Unused second parameter.
    :return: None. Prints the list of commands to the console.
    """
    quit_application()


def handle_show_movies(_, movies_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Display a list of all unique countries represented by ships in the dataset.

    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :param _: Unused parameter
    :return: None. Prints a sorted list of unique ship countries.
    """
    title = "Movie list"
    print_title(title, len(title))
    print_all_movies(movies_dict)


def handle_add_movie(_, movies_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Handles user input to add a new movie to the database,
    including its name, rating, and release year.

    :param _: Unused parameter
    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    new_movie_name = get_colored_input("Enter new movie name: ")
    new_movie_rating = get_colored_numeric_input_float(
        "Enter new movie rating (0-10): ", 0, 10
    )
    current_year = datetime.date.today().year
    new_movie_release = int(
        get_colored_numeric_input_float(
            "Enter new movie release year: ", FIRST_FILM_RELEASE, current_year
        )
    )

    attributes = {"rating": new_movie_rating, "release": new_movie_release}

    add_movie(movies_dict, new_movie_name, attributes)


def handle_delete_movie(_, movie_data: dict[str, dict[str, float | int]]) -> None:
    """
    Handles user input to delete a movie from the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_data: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    movie_to_delete = get_colored_input(
        "Enter the name of the movie you want to delete: "
    )
    delete_movie(movie_data, movie_to_delete)


def handle_update_movie(_, movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Handles user input to update the rating of a specific movie in the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    movie_name = find_movie(movie_dict)
    new_rating = get_colored_numeric_input_float(
        "Enter the new rating for the movie: ", RATING_BASE, RATING_LIMIT
    )
    update_movie(movie_dict, movie_name, "rating", new_rating)


def handle_show_movie_statistics(
    _, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Handles the process of calculating and displaying movie statistics,
    including average rating, median rating, best and worst movies.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries (e.g. rating, release).
    :return: None
    """
    average_rate = get_calculated_average_rate(movie_dict)
    median_rate = get_calculated_median_rate(movie_dict)

    best_movies = get_all_movies_extremes_by_mode(movie_dict, "best")
    worst_movies = get_all_movies_extremes_by_mode(movie_dict, "worst")

    print_movies_statistics(average_rate, median_rate, best_movies, worst_movies)


def handle_random_movie(_, movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Selects a random movie from the database and displays its details.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    random_movie = get_random_movie(movie_dict)
    title = list(random_movie.keys())[0]
    details = random_movie[title]
    print_movie(title, details)


def handle_search_movie(_, movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Handles the search functionality for finding movies by name.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    search_query = get_colored_input("Enter part of movie name:").lower()
    matches = filter_movies_by_search_query(movie_dict, search_query)
    print_search_results(matches)


def handle_sorted_movies_by_rating(
    _, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Handles the process of retrieving and displaying movies sorted by rating.

    Uses the provided movie dictionary to sort movies by their rating in descending
    order and prints the sorted list to the console.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries (e.g. rating, release).
    :return: None
    """
    sorted_movies = get_movies_sorted_by_attribute(movie_dict, "rating")
    print_movies(sorted_movies)


def handle_create_histogram_by_attribute(
    _, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Handles the creation and saving of a histogram for a user-selected attribute.

    Prompts the user to enter an attribute (e.g., "rating", "release") and a file name,
    then generates and saves the corresponding histogram. Repeats if the attribute is invalid.

    :param _: Unused parameter.
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    while True:
        attribute = get_colored_input(
            "Enter attribute to visualize (e.g., rating, release): "
        ).lower()
        if all(attribute in details for details in movie_dict.values()):
            break
        print_colored_output(
            f"❌ Attribute '{attribute}' not found in all movies. Try again.",
            COLOR_ERROR,
        )

    create_histogram_by_attribute(movie_dict, attribute)
