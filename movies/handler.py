"""
menu / handler.py

This module defines the handler functions responsible for managing all user interactions
in the SQL-based movies database application.

It works in conjunction with the MOVIE_COMMAND_DISPATCHER to map each menu option
to its respective behavior. These handlers implement the core application logic
such as movies management, statistics generation, data filtering, and external API interaction.

Main responsibilities include:
- Adding, deleting, updating, and listing movies records
- Displaying individual or random movies and their details
- Searching and sorting movies by user-defined attributes
- Computing and presenting statistical metrics (average, median, etc.)
- Creating visual representations such as rating histograms
- Filtering movies sets by rating and release year
- Generating a dynamic HTML website for favorite movies
- Managing movies notes and favorite flags per user
- Interfacing with the OMDb API for movies data retrieval
- Persisting user-specific movies data through SQL storage
- Enforcing user context for all operations
- Loading API configuration from a .env environment file

Author: Martin Haferanke
Date: 16.06.2025
"""

import requests

import movies
from helpers.file_utils import load_data, save_data
from helpers.filter_utils import (
    find_movie,
    filter_movies_by_search_query,
    filter_movies_by_attributes,
)
from helpers.html_utils import (
    replace_placeholder_with_html_content,
    generate_movie_html_content,
)
from helpers.input_utils import (
    get_colored_input,
    get_content_validated_input,
    get_input_by_type_and_range,
    get_current_year,
)
from helpers.movie_utils import parse_fields, extract_valid_attributes
from helpers.stats_utils import (
    get_movies_sorted_by_attribute,
    create_histogram_by_attribute,
)
from helpers.system_utils import quit_application
from movies import storage_sql
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

from users.session_user import abort_if_no_active_user, get_active_user

# Initialize .env to get API Key and API_URL for secure access
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = os.getenv("OMDB_API_URL")


def handle_quit_application(_, __, ___):
    """
    Quit the application after the user selects this option.

    :param _: Unused parameter.
    :param __: Unused second parameter.
    :param ___: Unused third parameter.
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

    movies_for_user = movies.storage_sql.list_movies(active_user_id)
    if not movies_for_user:
        return print_colored_output("❌ No movies available to show.", COLOR_ERROR)

    print_title(f"Movies for User ID {active_user_id}")
    return print_all_movies(movies_for_user)


def handle_add_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to add a new movies to the database, including its name, rating, and release year.

    Prompts the user to enter a movies title, retrieves data from the OMDb API,
    constructs the attribute dictionary, and updates both the in-memory and persistent storage.


    :param _: Unused parameter.
    :param movie_dict: dict[str, dict] – Dictionary of movies titles and their attribute dictionaries.
    :param ___: Unused parameter.
    :return: None. Prints success or error messages based on the outcome.
    """
    active_user_id = abort_if_no_active_user()
    new_movie_name = get_colored_input("Enter new movies name: ")

    if new_movie_name in movie_dict:
        return print_colored_output("❌ Movie already exists.", COLOR_ERROR)

    try:
        # Make API request to OMDb API and parse response
        req = requests.get(f"{OMDB_API_URL}&apikey={OMDB_API_KEY}&t={new_movie_name}")
        if req.status_code != 200:
            return print_colored_output("❌ API request failed.", COLOR_ERROR)

        data = req.json()

        if data.get("Response") == "False":
            return print_colored_output(
                f"❌ Movie '{new_movie_name}' not found in OMDb API.", COLOR_ERROR
            )

        required_fields = {
            "imdbRating": float,
            "Year": int,
            "imdbID": str,
            "Country": str,
        }

        try:
            parsed_data = parse_fields(data, required_fields)
        except ValueError as e:
            return print_colored_output(f"❌ {e}", COLOR_ERROR)

        # Construct attribute dictionary for movies
        rating = parsed_data["imdbRating"]
        year = parsed_data["Year"]
        imdb_id = parsed_data["imdbID"]
        country = parsed_data["Country"]

        attributes = {
            "rating": rating,
            "year": year,
            "poster_url": data["Poster"],
            "imdb_id": imdb_id,
            "country": country,
        }

        # Add movies to persistent storage
        storage_sql.add_movie(active_user_id, new_movie_name, attributes)

        # Refresh movie_dict from DB
        updated_movies = storage_sql.list_movies(active_user_id)
        if new_movie_name in updated_movies:
            movie_dict[new_movie_name] = updated_movies[new_movie_name]

        return None

    except Exception as e:
        return print_colored_output(f"❌ Failed to add movies. Error: {e}", COLOR_ERROR)


def handle_delete_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to delete a movies from the database.

    Prompts the user to enter a movies title. If the movies exists in the database,
    it will be removed from both the in-memory dictionary and persistent storage.

    :param _: Unused parameter (commonly required by handler interface).
    :param movie_dict: dict[str, dict] – Dictionary of movies titles and their attribute dictionaries.
    :return: None. Prints confirmation or error message depending on outcome.
    """
    active_user_id = abort_if_no_active_user()

    user_movies = movies.storage_sql.list_movies(active_user_id)

    if not user_movies:
        return print_colored_output("❌ No movies to delete.", COLOR_ERROR)

    movie_to_delete = get_colored_input(
        "Enter the name of the movies you want to delete: "
    )

    if movie_to_delete not in user_movies:
        return print_colored_output(
            f"❌ Movie '{movie_to_delete}' not found for active user.", COLOR_ERROR
        )

    try:
        # Remove from persistent storage
        movies.storage_sql.delete_movie(active_user_id, movie_to_delete)

        # Remove from in-memory dictionary
        movie_dict.pop(movie_to_delete, None)

        return print_colored_output(
            f"✅ Movie '{movie_to_delete}' successfully deleted.", COLOR_SUCCESS
        )

    except Exception as e:
        return print_colored_output(
            f"❌ Error deleting movies '{movie_to_delete}': {e}", COLOR_ERROR
        )


def handle_update_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles user input to update the rating of a specific movies in the database.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
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

        new_note = get_colored_input("Enter movies note: ", COLOR_TITLE)
        new_favourite = get_content_validated_input(
            "Is this one of your favourite movies? (Yes or No): ", {"Yes", "No"}
        )
        is_favourite = new_favourite == "Yes"

        # Update note and favourite movies in persistent storage
        movies.storage_sql.update_movie(
            active_user_id, movie_name, new_note, int(is_favourite)
        )

        # Refresh movie_dict from DB
        updated_movies = storage_sql.list_movies(active_user_id)
        if updated_movies and movie_name in updated_movies:
            movie_dict[movie_name] = updated_movies[movie_name]

        return print_colored_output(
            f"✅ Movie '{movie_name}' personal note and favourite updated to '{new_note}'.",
            COLOR_SUCCESS,
        )

    except Exception as e:
        return print_colored_output(f"❌ Error updating movies rating: {e}", COLOR_ERROR)


def handle_show_movie_statistics(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the process of calculating and displaying movies statistics,
    including average rating, median rating, best and worst movies.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries (e.g. rating, release).
    :return: None
    """
    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output(
            f"❌ No movies in database. Try to add a movies.", COLOR_ERROR
        )

    average_rate = get_calculated_average_rate(movie_dict)
    median_rate = get_calculated_median_rate(movie_dict)

    best_movies = get_all_movies_extremes_by_mode(movie_dict, "best")
    worst_movies = get_all_movies_extremes_by_mode(movie_dict, "worst")

    return print_movies_statistics(average_rate, median_rate, best_movies, worst_movies)


def handle_random_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Selects a random movies from the database and displays its details.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
    :return: None
    """

    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to print random one.", COLOR_ERROR
        )
    print_title("Random movies")
    random_movie = get_random_movie(movie_dict)
    title = list(random_movie.keys())[0]
    details = random_movie[title]
    return print_movie(title, details)


def handle_search_movie(_, movie_dict: dict[str, dict], ___) -> None:
    """
    Handles the search functionality for finding movies by name.

    :param _: Unused parameter (commonly required by menu handlers).
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
    :return: None
    """

    abort_if_no_active_user()

    if not movie_dict:
        return print_colored_output("❌ No movies to search for.", COLOR_ERROR)

    search_query = get_colored_input("Enter part of movies name:").lower()
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
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
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
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
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
    default values are used. The filtered movies list is then displayed based on these criteria.

    :param _: Unused parameter (required by handler interface).
    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
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
    such as a custom title and generated movies cards, and saves the final HTML output.

    :param _: Unused parameter (required by handler interface)
    :param movie_dict: dict[str, dict] – Dictionary of movies titles and their attribute dictionaries
    :return: None
    """

    abort_if_no_active_user()

    username = get_active_user()

    # Load the HTML template from file
    html_template = load_data(HTML_TEMPLATE_FILE)

    # Replace the title placeholder with the new content
    html_template = replace_placeholder_with_html_content(
        html_template, PLACEHOLDER_TITLE, f"{username}'s Movie App"
    )

    movie_card_html = generate_movie_html_content(movie_dict)

    # Replace the movies grid placeholder with the same content
    html_template = replace_placeholder_with_html_content(
        html_template, PLACEHOLDER_MOVIE_GRID, movie_card_html
    )
    # Save the new html content to an index.html file
    save_data(HTML_OUTPUT_FILE, html_template)
