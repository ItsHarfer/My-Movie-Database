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
from config import FIRST_FILM_RELEASE, RATING_BASE, RATING_LIMIT, COLOR_ERROR, DATA_FILE
from helpers import (
    quit_application,
    get_movies_sorted_by_attribute,
    get_colored_input,
    get_input_by_type_and_range,
    find_movie,
    filter_movies_by_search_query,
    create_histogram_by_attribute,
    get_current_year,
    get_content_validated_input,
    extract_valid_attributes,
    filter_movies_by_attributes,
)
from movie_crud import (
    add_movie,
    delete_movie,
    update_movie,
)
from movie_storage import save_movies, get_movie_list
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


def handle_show_movies(_, __) -> None:
    """
    Display a list of all unique countries represented by ships in the dataset.

    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :param _: Unused parameter
    :return: None. Prints a sorted list of unique ship countries.
    """
    movies = get_movie_list(DATA_FILE)
    print_title("Movie list")
    print_all_movies(movies)


def handle_add_movie(_, __) -> None:
    """
    Handles user input to add a new movie to the database,
    including its name, rating, and release year.

    :param __: Unused parameter
    :param _: Unused parameter
    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    new_movie_name = get_colored_input("Enter new movie name: ")
    new_movie_rating = get_input_by_type_and_range(
        f"Enter new movie rating ({RATING_BASE}-{RATING_LIMIT}): ",
        float,
        RATING_BASE,
        RATING_LIMIT,
    )
    current_year = get_current_year()
    new_movie_release = get_input_by_type_and_range(
        "Enter new movie release year: ", float, FIRST_FILM_RELEASE, current_year
    )

    attributes = {"rating": new_movie_rating, "release": new_movie_release}

    add_movie(new_movie_name, attributes)


def handle_delete_movie(_, __) -> None:
    """
    Handles user input to delete a movie from the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :return: None
    """
    movie_to_delete = get_colored_input(
        "Enter the name of the movie you want to delete: "
    )
    delete_movie(movie_to_delete)


def handle_update_movie(_, movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Handles user input to update the rating of a specific movie in the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    movie_name = find_movie(movie_dict)
    new_rating = get_input_by_type_and_range(
        "Enter the new rating for the movie: ", float, RATING_BASE, RATING_LIMIT
    )

    update_movie(movie_name, new_rating)


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


def handle_sorted_movies_by_attribute(
    _, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Handles the process of retrieving and displaying movies sorted by a selected attribute. (BONUS)

    Prompts the user to choose an attribute (any available in the dataset) and whether
    they want the results in descending ("first") or ascending ("last") order.
    Displays the sorted list of movies including their attributes.

    :param _: Unused parameter
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    if not movie_dict:
        print_colored_output("❌ No movies available to sort.", COLOR_ERROR)
        return

    valid_attributes = extract_valid_attributes(movie_dict)

    if not valid_attributes:
        print_colored_output(
            "❌ Could not determine available attributes.", COLOR_ERROR
        )
        return

    attribute = get_content_validated_input(
        f"Which attribute do you want to sort by? Available: {', '.join(valid_attributes)}: ",
        valid_attributes,
    )

    order = get_content_validated_input(
        f"Do you want to see the movies with the highest {attribute} first or last? (Enter 'first' or 'last'): ",
        {"first", "last"},
    )

    descending = order == "first"
    sorted_movies = get_movies_sorted_by_attribute(movie_dict, attribute, descending)
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
        )
        is_available_attribute = all(
            attribute in details for details in movie_dict.values()
        )

        if is_available_attribute:
            break
        print_colored_output(
            f"❌ Attribute '{attribute}' not found in all movies. Try again.",
            COLOR_ERROR,
        )

    create_histogram_by_attribute(movie_dict, attribute)


def handle_filter_movies(_, movie_dict) -> None:
    """
    Handles user input to filter movies by rating and release year range.

    Prompts the user for minimum rating, start year, and end year. If no input is provided,
    default values are used. The filtered movie list is then displayed based on these criteria.

    :param _: Unused parameter (required by handler interface).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    min_rating = (
        get_input_by_type_and_range(
            "Enter min rating (leave blank for no min rating): ",
            float,
            RATING_BASE,
            RATING_LIMIT,
            valid_empty_input=True,
        )
        or RATING_BASE
    )

    current_year = get_current_year()
    start_year = (
        get_input_by_type_and_range(
            "Enter start year (leave blank for no start year): ",
            int,
            FIRST_FILM_RELEASE,
            current_year,
            valid_empty_input=True,
        )
        or FIRST_FILM_RELEASE
    )

    end_year = (
        get_input_by_type_and_range(
            "Enter end year (leave blank for no end year): ",
            int,
            FIRST_FILM_RELEASE,
            current_year,
            valid_empty_input=True,
        )
        or current_year
    )

    filter_movies_by_attributes(movie_dict, min_rating, start_year, end_year)
