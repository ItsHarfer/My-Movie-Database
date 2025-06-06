"""
menu_handlers.py

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

Author: Martin Haferanke
Date: 06.06.2025
"""

import requests

from movie_storage import movie_storage_sql, data_io
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

# Initialize .env to get API Key and API_URL for secure access
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = os.getenv("OMDB_API_URL")


def handle_quit_application(_, __):
    """
    Quit the application after the user selects this option.

    :param _: Unused parameter.
    :param __: Unused second parameter.
    :return: None. Prints the list of commands to the console.
    """
    quit_application()


def handle_show_movies(_, movie_dict: dict[str, dict]) -> None:
    """
    Display a list of all unique countries represented by ships in the dataset.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :param _: Unused parameter
    :return: None. Prints a sorted list of unique ship countries.
    """
    if not movie_dict:
        return print_colored_output("❌ No movies available to show.", COLOR_ERROR)

    print_title("Movie list")
    return print_all_movies(movie_dict)


def handle_add_movie(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles user input to add a new movie to the database, including its name, rating, and release year.

    Prompts the user to enter a movie title, retrieves data from the OMDb API,
    constructs the attribute dictionary, and updates both the in-memory and persistent storage.

    :param _: Unused parameter (commonly required by handler interface).
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries.
    :return: None. Prints success or error messages based on the outcome.
    """
    new_movie_name = get_colored_input("Enter new movie name: ")

    if new_movie_name in movie_dict:
        return print_colored_output(
            "❌ Movie is already in the database. Try again.", COLOR_ERROR
        )

    try:
        # Fetch movie data from OMDb API by title
        req = requests.get(f"{OMDB_API_URL}&apikey={OMDB_API_KEY}&t={new_movie_name}")
        data = req.json()

        # Build the attribute dictionary using relevant data from API
        attributes = {
            "rating": float(data["imdbRating"]),
            "year": int(data["Year"]),
            "poster_url": data["Poster"],
        }

        # Update the local dictionary
        movie_dict[new_movie_name] = attributes

        # Save the new movie and its attributes to the database
        return movie_storage_sql.add_movie(new_movie_name, attributes)

    except (KeyError, ValueError, TypeError) as e:
        return print_colored_output(
            f"❌ Failed to process movie data. Error: {e}", COLOR_ERROR
        )
    except requests.RequestException as e:
        return print_colored_output(
            f"❌ Failed to reach OMDb API. Network error: {e}", COLOR_ERROR
        )


def handle_delete_movie(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles user input to delete a movie from the database.

    Prompts the user to enter a movie title. If the movie exists in the database,
    it will be removed from both the in-memory dictionary and persistent storage.

    :param _: Unused parameter (commonly required by handler interface).
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries.
    :return: None. Prints confirmation or error message depending on outcome.
    """
    if not movie_dict:
        return print_colored_output("❌ No movies to delete.", COLOR_ERROR)

    movie_to_delete = get_colored_input(
        "Enter the name of the movie you want to delete: "
    )

    # Check if the movie exists in the dictionary
    if movie_to_delete not in movie_dict:
        return print_colored_output(
            f"❌ Movie '{movie_to_delete}' not found in the database.", COLOR_ERROR
        )

    try:
        # Remove the movie from the in-memory dictionary
        del movie_dict[movie_to_delete]

        # Remove the movie from persistent storage
        movie_storage_sql.delete_movie(movie_to_delete)

        return print_colored_output(
            f"✅ Movie '{movie_to_delete}' successfully deleted.", COLOR_SUCCESS
        )

    except Exception as e:
        return print_colored_output(
            f"❌ Error deleting movie '{movie_to_delete}': {e}", COLOR_ERROR
        )


def handle_update_movie(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles user input to update the rating of a specific movie in the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    if not movie_dict:
        return print_colored_output("❌ No movies available to update.", COLOR_ERROR)

    try:
        movie_name = find_movie(movie_dict)

        if movie_name not in movie_dict:
            return print_colored_output(
                f"❌ Movie '{movie_name}' not found in the database.", COLOR_ERROR
            )

        new_rating = get_input_by_type_and_range(
            "Enter the new rating for the movie: ", float, RATING_BASE, RATING_LIMIT
        )

        # Update rating in memory
        movie_dict[movie_name]["rating"] = new_rating

        # Update rating in persistent storage
        movie_storage_sql.update_movie(movie_name, new_rating)

        return print_colored_output(
            f"✅ Movie '{movie_name}' rating updated to {new_rating}.",
            COLOR_SUCCESS,
        )

    except Exception as e:
        return print_colored_output(f"❌ Error updating movie rating: {e}", COLOR_ERROR)


def handle_show_movie_statistics(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles the process of calculating and displaying movie statistics,
    including average rating, median rating, best and worst movies.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries (e.g. rating, release).
    :return: None
    """

    if not movie_dict:
        return print_colored_output(
            f"❌ No movies in database. Try to add a movie.", COLOR_ERROR
        )

    average_rate = get_calculated_average_rate(movie_dict)
    median_rate = get_calculated_median_rate(movie_dict)

    best_movies = get_all_movies_extremes_by_mode(movie_dict, "best")
    worst_movies = get_all_movies_extremes_by_mode(movie_dict, "worst")

    return print_movies_statistics(average_rate, median_rate, best_movies, worst_movies)


def handle_random_movie(_, movie_dict: dict[str, dict]) -> None:
    """
    Selects a random movie from the database and displays its details.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to print random one.", COLOR_ERROR
        )
    print_title("Random movie")
    random_movie = get_random_movie(movie_dict)
    title = list(random_movie.keys())[0]
    details = random_movie[title]
    return print_movie(title, details)


def handle_search_movie(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles the search functionality for finding movies by name.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    if not movie_dict:
        return print_colored_output("❌ No movies to search for.", COLOR_ERROR)

    search_query = get_colored_input("Enter part of movie name:").lower()
    matches = filter_movies_by_search_query(movie_dict, search_query)
    print_title("Search results")
    return print_search_results(matches)


def handle_sorted_movies_by_attribute(_, movie_dict: dict[str, dict]) -> None:
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


def handle_create_histogram_by_attribute(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles the creation and saving of a histogram for a user-selected attribute.

    Prompts the user to enter an attribute (e.g., "rating", "year") and a file name,
    then generates and saves the corresponding histogram. Repeats if the attribute is invalid.

    :param _: Unused parameter.
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
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


def handle_filter_movies(_, movie_dict: dict[str, dict]) -> None:
    """
    Handles user input to filter movies by rating and release year range.

    Prompts the user for minimum rating, start year, and end year. If no input is provided,
    default values are used. The filtered movie list is then displayed based on these criteria.

    :param _: Unused parameter (required by handler interface).
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """

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


def handle_generate_website(_, movie_dict: dict[str, dict]) -> None:
    """
    Generates a website displaying the current list of movies.

    Loads an HTML template, replaces predefined placeholders with actual content
    such as a custom title and generated movie cards, and saves the final HTML output.

    :param _: Unused parameter (required by handler interface)
    :param movie_dict: dict[str, dict] – Dictionary of movie titles and their attribute dictionaries
    :return: None
    """
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
