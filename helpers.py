"""
helpers.py

Provides utility functions for the movie database application.

This module includes reusable helper functions for:
- handling colored user input and output,
- searching and sorting movie data,
- creating visualizations (e.g. rating histograms),
- quitting the application gracefully,
- validating numeric input,
- and finding specific movies in the dataset.

It acts as a support layer for the main application logic and improves code reuse,
readability, and maintainability.
"""

from datetime import datetime
import sys
from colorama import Style
from matplotlib import pyplot as plt

from config import (
    COLOR_MAP,
    COLOR_INPUT,
    COLOR_SUCCESS,
    COLOR_ERROR,
    HISTOGRAM_WIDTH,
    HISTOGRAM_HEIGHT,
)
from printers import print_colored_output, print_movies, print_title


def quit_application() -> None:
    """
    Exits the application.

    Prints a farewell message to the console and then terminates the program
    with a status code of 0 (successful exit).
    :return: None
    """
    print("Bye!")
    sys.exit(0)


def get_colored_input(prompt: str, color: str = COLOR_INPUT) -> str:
    """
    Prompts the user for input and output with colored text.

    :param prompt: Text shown to the user.
    :param color: Optional color name (default: 'light_magenta').
    :return: Trimmed user input as string.
    """
    color_prefix = COLOR_MAP.get(color, "")
    return input(color_prefix + prompt + Style.RESET_ALL).strip()


def get_type_validated_input(prompt: str, expected_type: type):
    while True:
        user_input = get_colored_input(prompt)
        try:
            return expected_type(user_input)
        except ValueError:
            print_colored_output(
                f"❌ Invalid input. Please enter a valid {expected_type.__name__}.",
                COLOR_ERROR,
            )


def get_content_validated_input(prompt: str, valid_options: set[str]) -> str:
    """
    Prompts the user for input and validates it against a set of allowed options.

    The input is displayed in color and repeated until a valid value is entered.

    :param prompt: The text to display to the user.
    :param valid_options: A set of accepted string values.
    :return: A validated and normalized user input string.
    """
    while True:
        user_input = get_colored_input(prompt)
        if user_input in valid_options:
            return user_input
        print_colored_output(
            f"❌ Invalid input '{user_input}'. Please enter one of: {', '.join(valid_options)}.",
            COLOR_ERROR,
        )


def filter_movies_by_search_query(
    movie_dict: dict[str, dict[str, float | int]], search_query: str
) -> dict:
    """
    Filters the movie dictionary for titles that contain the search query.

    Performs a case-insensitive substring search in all movie titles and returns
    a dictionary of matching entries.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :param search_query: Lowercase string to search for within movie titles.
    :return: Dictionary of matching movie titles and their attributes.
    """
    return {
        title: details
        for title, details in movie_dict.items()
        if search_query in title.lower()
    }


def filter_movies_by_attributes(
    movie_dict: dict[str, dict[str, float | int]],
    min_rating: float,
    start_year: int,
    end_year: int,
) -> None:
    """
    Filters and displays movies that match the specified rating and release year criteria.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries
    :param min_rating: Minimum rating a movie must have to be included.
    :param start_year: Earliest release year to include.
    :param end_year: Latest release year to include.
    :return: None
    """
    filtered_movies = {
        title: details
        for title, details in movie_dict.items()
        if details["rating"] >= min_rating
        and start_year <= details["release"] <= end_year
    }
    if not filtered_movies:
        print_colored_output(
            "🔍 No matching movies found. Try adjusting your filter.", COLOR_ERROR
        )
    else:
        print_title("Filtered movies")
        print_movies(filtered_movies)


def get_movies_sorted_by_attribute(
    movie_dict: dict[str, dict[str, float | int]], attribute: str, descending=True
) -> dict[str, dict[str, float | int]]:
    """
    Sorts the movies by a given numeric attribute.

    This function takes a dictionary of movies with their associated attributes and
    returns a new dictionary sorted by the specified attribute (e.g., rating, release year).

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries
    :param attribute: The key of the attribute to sort by (e.g. "rating", "year").
    :param descending: If True, sorts in descending order (highest to lowest).
                       If False, sorts in ascending order. Defaults to True.
    :return: A new dictionary of movies sorted by the given attribute.
    """
    attribute_value_key = lambda details: details[1][attribute]
    sorted_movie_dict = dict(
        sorted(movie_dict.items(), key=attribute_value_key, reverse=descending)
    )
    return sorted_movie_dict


def create_histogram_by_attribute(
    movie_dict: dict[str, dict[str, float | int]], attribute: str
) -> None:
    """
    Creates and saves a scatter plot for the 'release' attribute.
    For all other attributes, creates and saves a horizontal bar chart.

    :param movie_dict: Dictionary of movies and their attribute data.
    :param attribute: The attribute to visualize.
    """
    file_name = get_colored_input(f"✍️ Please name your histogram for '{attribute}': ")
    if not file_name.endswith(".png"):
        file_name += ".png"

    movie_names_list = list(movie_dict.keys())
    movie_attribute_list = [details[attribute] for details in movie_dict.values()]

    plt.figure(figsize=(HISTOGRAM_WIDTH, HISTOGRAM_HEIGHT))

    if attribute == "release":
        plt.scatter(movie_attribute_list, movie_names_list)
        plt.xlabel(attribute.capitalize())
        plt.ylabel("Movie")
        plt.title("Movie Release Years")
    else:
        plt.barh(movie_names_list, movie_attribute_list)
        plt.xlabel(attribute.capitalize())
        plt.ylabel("Movie")
        plt.title(f"Movie {attribute.capitalize()}s")

    plt.tight_layout()
    plt.savefig(file_name)
    print_colored_output(
        f'✅ Plot saved as "{file_name}" in your project files.',
        COLOR_SUCCESS,
    )


def get_input_by_type_and_range(
    prompt: str,
    datatype: type,
    start_range: float,
    end_range: float,
    valid_empty_input=False,
) -> float | None:
    """
    Prompts the user to enter a floating-point number within a specified range.
    The input is validated and an error message is shown if the input is invalid
    or out of range.

    :param valid_empty_input:
    :param datatype:
    :param prompt: The message shown to the user.
    :param start_range: The minimum acceptable value (inclusive).
    :param end_range: The maximum acceptable value (inclusive).
    :return: The validated floating-point number entered by the user.
    """
    while True:
        user_input = get_colored_input(prompt)
        if valid_empty_input and user_input == "":
            return None
        try:
            user_input_with_type = datatype(user_input)
            if start_range <= user_input_with_type <= end_range:
                return user_input_with_type
            else:
                print_colored_output(
                    f"❌ Please enter a value between {start_range} and {end_range}.",
                    COLOR_ERROR,
                )
        except ValueError:
            print_colored_output(
                "❌ Invalid input. Please enter a valid number.", COLOR_ERROR
            )


def get_current_year() -> int:
    return datetime.now().year


def find_movie(movie_dict: dict[str, dict]) -> str:
    """
    Prompts the user to enter a movie name and returns it if it exists in the database.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: The title of the movie entered by the user, if it exists in the dictionary.
    """
    while True:
        movie_to_update = get_colored_input(
            "Enter the name of the movie you want to update: "
        )
        if movie_to_update in movie_dict:
            print_colored_output(f'🔍 "{movie_to_update}" found! ', COLOR_SUCCESS)
            return movie_to_update
        else:
            print_colored_output("❌ Movie not found. Please try again.", COLOR_ERROR)


def extract_valid_attributes(movie_dict: dict[str, dict[str, float | int]]) -> set[str]:
    """
    Extracts a set of valid attribute names from the first movie entry in the dictionary.

    :param movie_dict: Dictionary of movie titles and their attributes.
    :return: Set of attribute names.
    """
    for attributes in movie_dict.values():
        if isinstance(attributes, dict):
            return set(attributes.keys())
    return set()
