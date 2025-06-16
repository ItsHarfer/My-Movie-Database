"""
helpers / analysis.py

Provides functionality for sorting and visualizing movies data based on numeric attributes.

This module enables statistical analysis and graphical representation of movies attributes,
such as rating or release year. It includes functionality for sorting movies and generating
histograms or scatter plots as PNG files.

Functions:
- get_movies_sorted_by_attribute: Sorts the movies dictionary by a specified numeric field.
- create_histogram_by_attribute: Generates and saves a histogram or scatter plot for a given attribute.

These utilities support deeper insights into the movies dataset by enabling data-driven exploration.

Author: Martin Haferanke
Date: 16.06.2025
"""

from matplotlib import pyplot as plt

from config.config import COLOR_ERROR, HISTOGRAM_WIDTH, HISTOGRAM_HEIGHT, COLOR_SUCCESS
from helpers.input_utils import get_colored_input
from printers import print_colored_output


def get_movies_sorted_by_attribute(
    movie_dict: dict[str, dict], attribute: str, descending=True
) -> dict[str, dict] | None:
    """
    Sorts the movies by a given numeric attribute.

    This function takes a dictionary of movies with their associated attributes and
    returns a new dictionary sorted by the specified attribute (e.g., rating, release year).

    :param movie_dict: Dictionary of movies titles and their attribute dictionaries
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
