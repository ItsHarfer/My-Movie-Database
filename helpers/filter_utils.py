"""
helpers / filter_utils.py

Provides filtering and search functionalities for the movies database.

This module enables users to search movies by title, filter them based on rating and release year,
and interactively find a movies by name. All user interactions are handled with consistent
CLI feedback using colored output.

Functions:
- filter_movies_by_search_query: Performs case-insensitive substring search in movies titles.
- filter_movies_by_attributes: Filters movies by rating and release year and prints the results.
- find_movie: Prompts the user to input a movies title and confirms its existence.

These tools enhance the user's ability to quickly locate and extract relevant movies data.

Author: Martin Haferanke
Date: 16.06.2025
"""

from config.config import COLOR_ERROR, COLOR_SUCCESS
from helpers.input_utils import get_colored_input
from printers import print_colored_output, print_title, print_movies


def filter_movies_by_search_query(
    movie_dict: dict[str, dict[str, float | int]], search_query: str
) -> dict:
    """
    Filters the movies dictionary for titles that contain the search query.

    Performs a case-insensitive substring search in all movies titles and returns
    a dictionary of matching entries.

    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
    :param search_query: Lowercase string to search for within movies titles.
    :return: Dictionary of matching movies titles and their attributes.
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

    :param movie_dict: Dictionary of movies titles and their attribute dictionaries
    :param min_rating: Minimum rating a movies must have to be included.
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


def find_movie(movie_dict: dict[str, dict]) -> str | None:
    """
    Prompts the user to enter a movies name and returns it if it exists in the database.

    Repeats input prompt until a matching movies title is found.

    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
    :return: The title of the selected movies, or None if no movies exist.
    """
    if not movie_dict:
        return print_colored_output(
            "❌ No movies available to looking for.", COLOR_ERROR
        )

    while True:
        movie_to_update = get_colored_input(
            "Enter the name of the movies you want to update: "
        )
        if movie_to_update not in movie_dict:
            print_colored_output("❌ Movie not found. Please try again.", COLOR_ERROR)
        else:
            print_colored_output(f'🔍 "{movie_to_update}" found! ', COLOR_SUCCESS)
            return movie_to_update
