"""
printers.py

Handles all formatted and colored output for the movie database application.

This module centralizes presentation logic, including:
- Displaying titles, prompts, and status messages with color
- Printing movie data, statistics, and search results
- Ensuring consistent visual formatting across the CLI

Separating these responsibilities helps maintain a clean structure and supports consistent UI behavior.

Author: Martin Haferanke
Date: 06.06.2025
"""

from colorama import Style

from config.config import (
    COLOR_MAP,
    COLOR_TEXT,
    COLOR_VALUES,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_TITLE,
    COLOR_SUB_TITLE,
)


def print_title(title_name: str) -> None:
    """
    Prints a formatted title surrounded by a given number of asterisks on each side.

    :param title_name: The title text to display.
    :return: None
    """
    star_count = len(title_name)
    print_asterix = f"*" * star_count
    print_colored_output(
        "\n" + print_asterix + f" {title_name} " + print_asterix, COLOR_TITLE
    )


def print_movie_count(total_movie_count: int) -> None:
    """
    Prints the total number of movies currently stored in the database.

    :param total_movie_count: Count of all movies in the data
    :return: None
    """
    print_colored_output(f"\n{total_movie_count} ", COLOR_VALUES, end="")
    print_colored_output("movies in total", COLOR_SUCCESS)


def print_all_movies(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Displays the total number of movies and prints each movie with its rating and release year.

    :param movie_dict: Dictionary of movie titles and their release years and ratings.
    :return: None
    """
    total_movie_count = len(movie_dict)
    print_movie_count(total_movie_count)
    print_movies(movie_dict)


def print_colored_output(prompt: str, color: str = COLOR_TEXT, end: str = "\n") -> None:
    """
    Prints the given text in the specified color using ANSI escape codes via colorama.

    :param prompt: The text to be displayed.
    :param color: The name of the color (default: 'cyan').
    :param end: End character for the print statement (default: new line).
    :return: None
    """
    color_prefix = COLOR_MAP.get(color, "")
    print(color_prefix + prompt + Style.RESET_ALL, end=end)


def print_movies_statistics(
    average_rate: float,
    median_rate: float,
    best_movies: dict[str, dict[str, float | int]],
    worst_movies: dict[str, dict[str, float | int]],
) -> None:
    """
    Displays statistics about the movies in the database,
    including average rating, median rating, best and worst movies.

    :param average_rate: The average rating of all movies.
    :param median_rate: The median rating of all movies.
    :param best_movies: Dictionary of the best-rated movie(s) and their attributes.
    :param worst_movies: Dictionary of the worst-rated movie(s) and their attributes.
    :return: None
    """
    print_title("Movie Statistics")
    print_colored_output(f"Average rating: ", COLOR_SUB_TITLE, end="")
    print_colored_output(f"{average_rate:.1f}", COLOR_VALUES)

    print_colored_output(f"Median rating: ", COLOR_SUB_TITLE, end="")
    print_colored_output(f"{median_rate:.1f}", COLOR_VALUES)

    print_colored_output(f"Best movie(s): ", COLOR_SUB_TITLE)
    print_movies(best_movies)

    print_colored_output(f"Worst movie(s): ", COLOR_SUB_TITLE)
    print_movies(worst_movies)


def print_movie(title: str, movie: dict) -> None:
    """
    Displays a formatted line with the movie's title, release year, and rating.

    :param title: The title of the movie.
    :param movie: Dictionary containing movie attributes like 'release', 'rating', and optional others.
    :return: None
    """
    year = movie.get("year", "unknown")
    rating = movie.get("rating", "unrated")
    poster_url = movie.get("poster_url", "unknown")

    print_colored_output(f"- {title} ({year}): ", COLOR_TITLE, end="")
    print_colored_output(f"{rating} ", COLOR_VALUES, end="")
    print_colored_output(f"Poster: {poster_url}", COLOR_SUCCESS)


def print_movies(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Prints movie(s) and their ratings from the given dictionary.

    :param movie_dict: Dictionary of movie titles and their details.
    """
    if not movie_dict:
        print_colored_output("❌ No movies to print.", COLOR_ERROR)
    else:
        for title, details in movie_dict.items():
            print_movie(title, details)


def print_search_results(matches: dict[str, dict[str, float | int]]) -> None:
    """
    Prints the search results or a message if no match is found.

    :param matches: Dictionary of matched movie titles and their attributes.
    :return: None
    """
    if not matches:
        print_colored_output("❌ No search result.", COLOR_ERROR)
    else:
        print_movies(matches)
