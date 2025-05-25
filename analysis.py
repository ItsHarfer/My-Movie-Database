"""
analysis.py

Provides statistical and evaluation functions for the movie database application.

This module includes logic for calculating:
- Average and median rating
- Movies with the highest or lowest rating
- Random movie selection
- Summing arbitrary numeric attributes

All functions are read-only and operate on the movie dictionary without modifying it.

These are used primarily by handler functions to present insights and statistics to the user.
"""

from random import Random

import printers as printer


def get_calculated_average_rate(movie_dict: dict[str, dict[str, float | int]]) -> float:
    """
    Calculates the average rating of all movies.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Float average rating.
    """
    return get_sum(movie_dict, "rating") / len(movie_dict)


def get_sum(movie_dict: dict[str, dict[str, float | int]], attribute: str) -> float:
    """
    Calculates the total sum of all values for the given attribute across all movies.

    :param movie_dict: Dictionary of movies and their attribute dictionaries.
    :param attribute: The attribute whose values should be summed (e.g., 'rating', 'release').
    :return: Float sum of all values for the specified attribute.
    :rtype: float
    """
    return sum(details[attribute] for details in movie_dict.values())


def get_calculated_median_rate(movie_dict: dict[str, dict[str, float | int]]) -> float:
    """
    Calculates the median rating of all movies in the database.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: The median rating as a float.
    """

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
    :param mode: Either 'best' or 'worst'.
    :return: Dictionary of matched movies and their details.
    """
    if not movie_dict:
        return None

    if mode == "best":
        extreme_rating = max(details["rating"] for details in movie_dict.values())
    elif mode == "worst":
        extreme_rating = min(details["rating"] for details in movie_dict.values())
    else:
        printer.print_colored_output('Mode must be "best" or "worst".', "red")
        return None

    return {
        title: details
        for title, details in movie_dict.items()
        if details["rating"] == extreme_rating
    }


def get_random_movie(
    movie_dict: dict[str, dict[str, float | int]],
) -> dict[str, dict[str, float | int]]:
    """
    Selects a random movie from the database.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Tuple (movie_name, movie_rating).
    """
    movies_as_list = list(movie_dict.items())
    random_index = Random().randint(0, len(movies_as_list) - 1)
    title, details = movies_as_list[random_index]
    return {title: details}
