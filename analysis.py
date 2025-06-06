"""
analysis.py

Provides statistical and analytical functions for the movie database application.

This module includes logic for calculating key metrics and insights such as:
- Average and median movie ratings
- Movies with the highest or lowest ratings
- Random movie selection
- Summation of arbitrary numeric attributes

These functions are read-only and do not modify the provided movie dictionary.

They are primarily invoked by handler functions to generate statistics and analysis
outputs for user-facing features.

Author: Martin Haferanke
Date: 25.05.2025
"""

from random import Random
import printers as printer
from config import COLOR_ERROR


def get_calculated_average_rate(
    movie_dict: dict[str, dict[str, float | int]],
) -> float | None:
    """
    Calculates the average rating of all movies.

    :param movie_dict: Dictionary of movies and ratings.
    :return: The average rating as float, or None if the input is empty.
    """
    if not movie_dict:
        return printer.print_colored_output(
            "❌ No movies in database to calculate.", COLOR_ERROR
        )

    return get_sum(movie_dict, "rating") / len(movie_dict)


def get_sum(
    movie_dict: dict[str, dict[str, float | int]], attribute: str
) -> int | None:
    """
    Calculates the total sum of all values for the given attribute across all movies.

    :param movie_dict: Dictionary of movies and their attribute dictionaries.
    :param attribute: The attribute whose values should be summed (e.g., 'rating', 'release').
    :return: The sum of all values for the specified attribute as int or float, or None if the input is empty.
    """
    if not movie_dict:
        return printer.print_colored_output(
            "❌ No movies in database to calculate.", COLOR_ERROR
        )

    return sum(details[attribute] for details in movie_dict.values())


def get_calculated_median_rate(
    movie_dict: dict[str, dict[str, float | int]],
) -> None | float | int:
    """
    Calculates the median rating of all movies in the database.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: The median rating as a float or int, or None if the input is empty.
    """
    if not movie_dict:
        return printer.print_colored_output(
            "❌ No movies in database to calculate.", COLOR_ERROR
        )

    sorted_rate_list = sorted(
        list(details["rating"] for details in movie_dict.values())
    )
    movies_in_database = len(movie_dict)

    # Check if the number of movies is odd or even
    if movies_in_database % 2 == 1:
        middle_index = movies_in_database // 2
        median = sorted_rate_list[middle_index]
    else:
        left_middle_index = movies_in_database // 2 - 1
        right_middle_index = movies_in_database // 2
        left_value = sorted_rate_list[left_middle_index]
        right_value = sorted_rate_list[right_middle_index]
        median = (left_value + right_value) / 2

    return median


def get_all_movies_extremes_by_mode(
    movie_dict: dict[str, dict[str, float | int]], mode: str
) -> dict[str, dict[str, float | int]] | None:
    """
    Finds all movies with either the highest or lowest rating.

    :param movie_dict: Dictionary of movies and their details.
    :param mode: Mode to search for extremes, must be either "best" or "worst".
    :return: Dictionary of matched movies and their details, or None if the input is empty or mode is invalid.
    """
    if not movie_dict:
        return printer.print_colored_output(
            "❌ No movies in database to calculate.", COLOR_ERROR
        )

    ratings = (details["rating"] for details in movie_dict.values())

    if mode == "best":
        extreme_rating = max(ratings)
    elif mode == "worst":
        extreme_rating = min(ratings)
    else:
        printer.print_colored_output('Mode must be "best" or "worst".', COLOR_ERROR)
        return None

    return {
        title: details
        for title, details in movie_dict.items()
        if details["rating"] == extreme_rating
    }


def get_random_movie(
    movie_dict: dict[str, dict[str, float | int]],
) -> dict[str, dict[str, float | int]] | None:
    """
    Selects a random movie from the database.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Dictionary containing one randomly selected movie and its details, or None if the input is empty.
    """
    if not movie_dict:
        return printer.print_colored_output(
            "❌ No movies in database to calculate.", COLOR_ERROR
        )

    movies_as_list = list(movie_dict.items())
    random_index = (
        Random().randint(0, len(movies_as_list) - 1) if len(movies_as_list) >= 1 else 0
    )
    title, details = movies_as_list[random_index]
    return {title: details}
