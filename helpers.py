"""
helpers.py

Provides utility functions for input handling, data filtering, visualization,
and HTML rendering in the movie database application.

This module includes reusable helper functions for:
- Colored user input and output
- Type and content validation of user input
- Searching, filtering, and sorting movie dictionaries
- Generating statistics and rating histograms
- Rendering and saving HTML files with movie data
- Exiting the application gracefully

It supports clean modularization of utility logic and enhances maintainability and code reuse.

Author: Martin Haferanke
Date: 13.06.2025
"""

from datetime import datetime
import sys

from colorama import Style
from matplotlib import pyplot as plt

from config.config import (
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


def get_type_validated_input(prompt: str, expected_type: type) -> int | float | str:
    """
    Prompts the user for input and converts it to the expected type.

    Repeats until the input can be converted to the given data type (e.g., int, float, str).
    Displays an error message for invalid conversions.

    :param prompt: Text shown to the user.
    :param expected_type: The expected Python type.
    :return: The input value converted to the expected type.
    """
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
    if not movie_dict:
        print_colored_output("⚠️ No movies available to search.", COLOR_ERROR)
        return {}

    return {
        title: details
        for title, details in movie_dict.items()
        if search_query in title.lower()
    }


def filter_movies_by_attributes(
    movie_dict: dict[str, dict],
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
    if not movie_dict:
        return print_colored_output("❌ No movies available to filter.", COLOR_ERROR)

    filtered_movies = {
        title: details
        for title, details in movie_dict.items()
        if details["rating"] >= min_rating and start_year <= details["year"] <= end_year
    }
    if not filtered_movies:
        print_colored_output(
            "🔍 No matching movies found. Try adjusting your filter.", COLOR_ERROR
        )
        return None
    else:
        print_title("Filtered movies")
        print_movies(filtered_movies)
        return None


def get_movies_sorted_by_attribute(
    movie_dict: dict[str, dict], attribute: str, descending=True
) -> dict[str, dict] | None:
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
    if not movie_dict:
        return print_colored_output("❌ No movies available to sort.", COLOR_ERROR)

    attribute_value_key = lambda details: details[1][attribute]
    sorted_movie_dict = dict(
        sorted(movie_dict.items(), key=attribute_value_key, reverse=descending)
    )
    return sorted_movie_dict


def create_histogram_by_attribute(movie_dict: dict[str, dict], attribute: str) -> None:
    """
    Creates and saves a scatter plot for the 'release' attribute.
    For all other attributes, creates and saves a horizontal bar chart.

    :param movie_dict: Dictionary of movies and their attribute data.
    :param attribute: The attribute to visualize.
    """
    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to create a histogram.", COLOR_ERROR
        )

    file_name = get_colored_input(f"✍️ Please name your histogram for '{attribute}': ")
    if not file_name.endswith(".png"):
        file_name += ".png"

    movie_names_list = list(movie_dict.keys())
    movie_attribute_list = [details[attribute] for details in movie_dict.values()]

    plt.figure(figsize=(HISTOGRAM_WIDTH, HISTOGRAM_HEIGHT))

    if attribute == "year":
        plt.scatter(movie_attribute_list, movie_names_list)
        plt.xlabel(attribute.capitalize())
        plt.ylabel("Movie")
        plt.title("Movie Release Years")

        # Show the years just in full years
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    else:
        plt.barh(movie_names_list, movie_attribute_list)
        plt.xlabel(attribute.capitalize())
        plt.ylabel("Movie")
        plt.title(f"Movie {attribute.capitalize()}s")

    plt.tight_layout()
    plt.savefig(file_name)
    return print_colored_output(
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

    :param valid_empty_input: If True, allows an empty string input and returns None.
    :param datatype: The datatype to cast for
    :param prompt: The message shown to the user.
    :param start_range: The minimum acceptable value (inclusive).
    :param end_range: The maximum acceptable value (inclusive).
    :return: A validated number of the specified type or None (if empty input is allowed).
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
    """
    Returns the current calendar year as a four-digit integer.

    Uses the system's current date and time to extract the year.

    :return: The current year
    """
    return datetime.now().year


def find_movie(movie_dict: dict[str, dict]) -> str | None:
    """
    Prompts the user to enter a movie name and returns it if it exists in the database.

    Repeats input prompt until a matching movie title is found.

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: The title of the selected movie, or None if no movies exist.
    """
    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to looking for.", COLOR_ERROR
        )

    while True:
        movie_to_update = get_colored_input(
            "Enter the name of the movie you want to update: "
        )
        if movie_to_update not in movie_dict:
            print_colored_output("❌ Movie not found. Please try again.", COLOR_ERROR)
        else:
            print_colored_output(f'🔍 "{movie_to_update}" found! ', COLOR_SUCCESS)
            return movie_to_update


def extract_valid_attributes(movie_dict: dict[str, dict]) -> set[str]:
    """
    Extracts a set of valid attribute names from the first movie entry in the dictionary.

    Returns an empty set if the dictionary is empty or invalid.

    :param movie_dict: Dictionary of movie titles and their attributes.
    :return: Set of attribute names.
    """
    if not movie_dict:
        print_colored_output("❌ No movies available with attributes.", COLOR_ERROR)
        return set()

    for attributes in movie_dict.values():
        if isinstance(attributes, dict):
            return set(attributes.keys())
    return set()


def replace_placeholder_with_html_content(
    html: str, placeholder: str, output: str
) -> str:
    """
    Replaces a placeholder string in the given HTML content with the specified output.

    This is typically used to inject dynamic content (e.g. movie title, movie grid)
    into a predefined HTML template.

    :param html: The original HTML string containing the placeholder.
    :param placeholder: The placeholder string to be replaced (e.g. {{__PLACEHOLDER_TITLE__}}).
    :param output: The string to replace the placeholder with.
    :return: HTML string with the placeholder replaced by the output.
    """

    if placeholder not in html:
        print_colored_output(
            f"❌ Error: Placeholder '{placeholder}' not found in HTML template.",
            COLOR_ERROR,
        )
        return html
    return html.replace(placeholder, output)


def generate_movie_html_content(movie_data: dict[str, dict]) -> str:
    """
    Generates HTML markup for a list of movies based on the given movie data.

    Iterates through each movie entry and serializes it into an HTML list item
    using the `serialize_movie` function, wrapping all items in an ordered list container.

    :param movie_data: Dictionary of movie titles and their corresponding attribute dictionaries.
    :return: HTML string containing the formatted movie cards.
    """
    output = ""
    output += '<ol class="movie-grid">'
    for title, details in movie_data.items():
        movie_dict = details.copy()
        movie_dict["title"] = title
        output += serialize_movie(movie_dict)
    output += "</ol>"
    return output


def serialize_movie(movie_obj: dict) -> str:
    """
    Serializes a movie dictionary into an HTML card string.

    Extracts the movie's title, year, rating, and poster URL and passes them to
    the `generate_movie_card` function to produce the final HTML markup.

    :param movie_obj: Dictionary containing the movie's attributes, including title, year, rating, and poster URL.
    :return: A string of HTML representing the serialized movie card.
    """
    title = movie_obj.get("title", "")
    year = movie_obj.get("year", "Unknown")
    rating = movie_obj.get("rating", "Unknown")
    note = movie_obj.get("note", "")
    poster_url = movie_obj.get("poster_url", "Unknown")
    imdb_id = movie_obj.get("imdb_id", "")
    imdb_url = f"https://www.imdb.com/title/{imdb_id}"
    return generate_movie_card(title, year, rating, note, poster_url, imdb_url)


def generate_movie_card(
    title: str,
    year: str | int,
    rating: str | float,
    note: str,
    poster_url: str,
    imdb_url: str,
) -> str:
    """
    Generates an HTML list item representing a movie card.

    Formats the provided movie data into a styled HTML snippet.

    :param note: Users preferred note about the movie.
    :param title: The title of the movie.
    :param year: The release year of the movie.
    :param rating: The IMDb rating of the movie.
    :param poster_url: URL of the movie poster image.
    :param imdb_url: URL to the movie's IMDb page.
    :return: HTML string for the movie card.
    """
    output = ""
    output += f"<li>\n"
    output += f'  <div class="movie">\n'
    output += f'    <div class="poster-wrapper" title="{note}">\n'
    output += f'      <a href="{imdb_url}" target="_blank">\n'
    output += f'        <img class="movie-poster" src="{poster_url}" alt="{title}">\n'
    output += f"      </a>\n"
    output += f"    </div>\n"
    output += f'    <div class="movie-title">{title}</div>\n'
    output += f'    <div class="movie-year">{year}</div>\n'
    output += f'    <div class="movie-rating-stars" style="--rating:{rating}" title="{rating}/10"></div>\n'
    output += f"  </div>\n"
    output += f"</li>\n"
    return output


def execute_operation(user_input: int, data: dict, dispatcher: dict[int, dict]) -> bool:
    """
    Executes the selected command from the user by invoking the corresponding handler out from the dispatcher.

    :param user_input: Index of the selected menu command.
    :param data: Context data passed to the handler (e.g., user or movie data).
    :param dispatcher: Mapping of menu indices to command handler definitions.
    :return: True if the handler was successfully executed, False otherwise.
    """
    command_data = dispatcher.get(user_input)
    if not command_data:
        print_colored_output(
            f"Unknown command '{user_input}'. Please select a valid option.",
            COLOR_ERROR,
        )
        return False

    args = command_data.get("args", [])
    result = command_data["handler"](None, data, args)

    return bool(result)
