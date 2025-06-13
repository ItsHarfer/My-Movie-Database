"""
handlers.py

This module defines handler functions for user interactions in the movie database application.

It is used in conjunction with the MOVIE_COMMAND_DISPATCHER, which maps user-selected
menu options to the corresponding handler logic.

Main features include:
- Adding, deleting, and updating movie records
- Listing all movies and showing individual or random entries
- Searching and sorting movie data by user-selected attributes
- Calculating and displaying statistics like average and median ratings
- Generating visualizations such as rating histograms
- Filtering movies based on rating and year range
- Generating a website with movie data
- Gracefully exiting the program
- Using the OMDb API to fetch movie data
- Managing user-specific movie storage and requiring an active user context
- Loading API keys and endpoints from a .env file

Author: Martin Haferanke
Date: 13.06.2025
"""

import requests

import movie_storage
from movie_storage import storage_sql, data_io
from analysis import (
    get_calculated_average_rate,
    get_calculated_median_rate,
    get_all_movies_extremes_by_mode,
    get_random_movie,
)
from config.config import (
    FIRST_MOVIE_RELEASE,
    RATING_BASE,
    RATING_LIMIT,
    COLOR_ERROR,
    COLOR_SUCCESS,
    HTML_TEMPLATE_FILE,
    PLACEHOLDER_TITLE,
    PLACEHOLDER_MOVIE_GRID,
    HTML_OUTPUT_FILE,
    COLOR_TITLE,
)
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
    replace_placeholder_with_html_content,
    generate_movie_html_content,
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

from dotenv import load_dotenv
import os

from users.users import abort_if_no_active_user

# Initialize .env to get API Key and API_URL for secure access
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = os.getenv("OMDB_API_URL")


def handle_quit_application(_, __, ___):
    """
    Quit the application after the user selects this option.

    :param _: Unused parameter.
    :param __: Unused second parameter.
    :return: None. Prints the list of commands to the console.
    """
    quit_application()


def handle_show_movies(_, __, ___) -> None:
    """
    Displays all movies stored for the currently active user.

    Fetches movies from persistent storage using the active user ID
    and prints them in a formatted list.

    :param _: Unused parameter.
    :param __: Unused parameter.
    :param ___: Unused parameter.
    :return: None
    """
    active_user_id = abort_if_no_active_user()

    movies_for_user = movie_storage.storage_sql.list_movies(active_user_id)
    if not movies_for_user:
        return print_colored_output("❌ No movies available to show.", COLOR_ERROR)

    print_title(f"Movies for User ID {active_user_id}")
    return print_all_movies(movies_for_user)


def handle_add_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to add a new movie to the database, including its name, rating, and release year.

    Prompts the user to enter a movie title, retrieves data from the OMDb API,
    constructs the attribute dictionary, and updates both the in-memory and persistent storage.

    :param _: Unused parameter (commonly required by handler interface).
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries.
    :return: None. Prints success or error messages based on the outcome.
    """
    active_user_id = abort_if_no_active_user()

    new_movie_name = get_colored_input("Enter new movie name: ")

    if new_movie_name in movie_dict:
        return print_colored_output("❌ Movie already exists.", COLOR_ERROR)

    try:
        req = requests.get(f"{OMDB_API_URL}&apikey={OMDB_API_KEY}&t={new_movie_name}")
        if req.status_code != 200:
            return print_colored_output("❌ API request failed.", COLOR_ERROR)

        data = req.json()

        if data.get("Response") == "False":
            return print_colored_output(
                f"❌ Movie '{new_movie_name}' not found in OMDb API.", COLOR_ERROR
            )

        if not all(k in data for k in ("imdbRating", "Year", "Poster")):
            return print_colored_output(
                "❌ Incomplete data received from API.", COLOR_ERROR
            )

        try:
            rating = float(data["imdbRating"])
        except (ValueError, TypeError):
            return print_colored_output(
                f"❌ Invalid rating value for movie '{new_movie_name}'.", COLOR_ERROR
            )

        try:
            year = int(data["Year"])
        except (ValueError, TypeError):
            return print_colored_output(
                f"❌ Invalid year value for movie '{new_movie_name}'.", COLOR_ERROR
            )

        attributes = {
            "rating": rating,
            "year": year,
            "poster_url": data["Poster"],
        }

        movie_dict[new_movie_name] = attributes

        return storage_sql.add_movie(active_user_id, new_movie_name, attributes)

    except Exception as e:
        return print_colored_output(f"❌ Failed to add movie. Error: {e}", COLOR_ERROR)


def handle_delete_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to delete a movie from the database.

    Prompts the user to enter a movie title. If the movie exists in the database,
    it will be removed from both the in-memory dictionary and persistent storage.

    :param _: Unused parameter (commonly required by handler interface).
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries.
    :return: None. Prints confirmation or error message depending on outcome.
    """
    active_user_id = abort_if_no_active_user()

    user_movies = movie_storage.storage_sql.list_movies(active_user_id)

    if not user_movies:
        return print_colored_output("❌ No movies to delete.", COLOR_ERROR)

    movie_to_delete = get_colored_input(
        "Enter the name of the movie you want to delete: "
    )

    if movie_to_delete not in user_movies:
        return print_colored_output(
            f"❌ Movie '{movie_to_delete}' not found for active user.", COLOR_ERROR
        )

    try:
        # Remove from in-memory dictionary if present
        movie_dict.pop(movie_to_delete, None)

        # Remove from persistent storage
        movie_storage.storage_sql.delete_movie(active_user_id, movie_to_delete)

        return print_colored_output(
            f"✅ Movie '{movie_to_delete}' successfully deleted.", COLOR_SUCCESS
        )

    except Exception as e:
        return print_colored_output(
            f"❌ Error deleting movie '{movie_to_delete}': {e}", COLOR_ERROR
        )


def handle_update_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to update the rating of a specific movie in the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    active_user_id = abort_if_no_active_user()

    user_movies = storage_sql.list_movies(active_user_id)

    if not user_movies:
        return print_colored_output("❌ No movies available to update.", COLOR_ERROR)

    try:
        movie_name = find_movie(user_movies)

        if movie_name not in user_movies:
            return print_colored_output(
                f"❌ Movie '{movie_name}' not found for the active user.", COLOR_ERROR
            )

        new_note = get_colored_input("Enter movie note: ", COLOR_TITLE)

        # Update note in memory
        movie_dict[movie_name]["note"] = new_note

        # Update rating in persistent storage
        movie_storage.storage_sql.update_movie(active_user_id, movie_name, new_note)

        return print_colored_output(
            f"✅ Movie '{movie_name}' personal note updated to '{new_note}'.",
            COLOR_SUCCESS,
        )

    except Exception as e:
        return print_colored_output(f"❌ Error updating movie rating: {e}", COLOR_ERROR)


def handle_show_movie_statistics(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the process of calculating and displaying movie statistics,
    including average rating, median rating, best and worst movies.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries (e.g. rating, release).
    :return: None
    """
    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output(
            f"❌ No movies in database. Try to add a movie.", COLOR_ERROR
        )

    average_rate = get_calculated_average_rate(movie_dict)
    median_rate = get_calculated_median_rate(movie_dict)

    best_movies = get_all_movies_extremes_by_mode(movie_dict, "best")
    worst_movies = get_all_movies_extremes_by_mode(movie_dict, "worst")

    return print_movies_statistics(average_rate, median_rate, best_movies, worst_movies)


def handle_random_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Selects a random movie from the database and displays its details.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """

    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to print random one.", COLOR_ERROR
        )
    print_title("Random movie")
    random_movie = get_random_movie(movie_dict)
    title = list(random_movie.keys())[0]
    details = random_movie[title]
    return print_movie(title, details)


def handle_search_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the search functionality for finding movies by name.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """

    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output("❌ No movies to search for.", COLOR_ERROR)

    search_query = get_colored_input("Enter part of movie name:").lower()
    matches = filter_movies_by_search_query(movie_dict, search_query)
    print_title("Search results")
    return print_search_results(matches)


def handle_sorted_movies_by_attribute(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the process of retrieving and displaying movies sorted by a selected attribute. (BONUS)

    Prompts the user to choose an attribute (any available in the dataset) and whether
    they want the results in descending ("first") or ascending ("last") order.
    Displays the sorted list of movies including their attributes.

    :param _: Unused parameter
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output("❌ No movies available to sort.", COLOR_ERROR)

    valid_attributes = extract_valid_attributes(movie_dict)

    if not valid_attributes:
        return print_colored_output(
            "❌ Could not determine available attributes.", COLOR_ERROR
        )

    attribute = get_content_validated_input(
        f"Which attribute do you want to sort by? Available: {', '.join(valid_attributes)}: ",
        valid_attributes,
    )

    order = get_content_validated_input(
        f"Do you want to see the movies with the highest {attribute} first or last? "
        f"(Enter 'first' or 'last'): ",
        {"first", "last"},
    )

    descending = order == "first"
    sorted_movies = get_movies_sorted_by_attribute(movie_dict, attribute, descending)

    print_title("Sorted movies")
    return print_movies(sorted_movies)


def handle_create_histogram_by_attribute(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the creation and saving of a histogram for a user-selected attribute.

    Prompts the user to enter an attribute (e.g., "rating", "year") and a file name,
    then generates and saves the corresponding histogram. Repeats if the attribute is invalid.

    :param _: Unused parameter.
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to create a histogram.", COLOR_ERROR
        )

    while True:
        attribute = get_colored_input(
            "Enter attribute to visualize (e.g., rating, year): "
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

    return create_histogram_by_attribute(movie_dict, attribute)


def handle_filter_movies(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to filter movies by rating and release year range.

    Prompts the user for minimum rating, start year, and end year. If no input is provided,
    default values are used. The filtered movie list is then displayed based on these criteria.

    :param _: Unused parameter (required by handler interface).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """

    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output("❌ No movies available to filter.", COLOR_ERROR)

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
            FIRST_MOVIE_RELEASE,
            current_year,
            valid_empty_input=True,
        )
        or FIRST_MOVIE_RELEASE
    )

    end_year = (
        get_input_by_type_and_range(
            "Enter end year (leave blank for no end year): ",
            int,
            FIRST_MOVIE_RELEASE,
            current_year,
            valid_empty_input=True,
        )
        or current_year
    )

    return filter_movies_by_attributes(movie_dict, min_rating, start_year, end_year)


def handle_generate_website(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Generates a website displaying the current list of movies.

    Loads an HTML template, replaces predefined placeholders with actual content
    such as a custom title and generated movie cards, and saves the final HTML output.

    :param _: Unused parameter (required by handler interface)
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries
    :return: None
    """

    abort_if_no_active_user()

    # Load the HTML template from file
    html_template = data_io.load_data(HTML_TEMPLATE_FILE)

    # Replace the title placeholder with the new content
    html_template = replace_placeholder_with_html_content(
        html_template, PLACEHOLDER_TITLE, "My Movie App"
    )

    movie_card_html = generate_movie_html_content(movie_dict)

    # Replace the movie grid placeholder with the same content
    html_template = replace_placeholder_with_html_content(
        html_template, PLACEHOLDER_MOVIE_GRID, movie_card_html
    )
    # Save the new html content to an index.html file
    data_io.save_data(HTML_OUTPUT_FILE, html_template)
