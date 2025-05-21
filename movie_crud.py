# =====================================================
# 🟢 CRUD Functions – Add, delete, update movies
# =====================================================
import datetime
from random import Random

from helpers import (
    get_colored_input,
    get_colored_numeric_input_float,
    get_movie_from_database,
    get_valid_movie_rating,
)
from printers import print_colored_output


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


def add_movie_to_database(movie_dict: dict[str, dict]) -> None:
    """
    Adds a new movie with its rating to the movie dictionary.

    :param movie_dict: Dictionary of movies and their ratings.
    :return: None
    """

    new_movie_name = get_colored_input("Enter new movie name: ")
    new_movie_rating = get_colored_numeric_input_float(
        "Enter new movie rating (0-10): ", 0, 10
    )
    current_year = datetime.date.today().year
    new_movie_release = int(
        get_colored_numeric_input_float(
            "Enter new movie release year: ", 1888, current_year
        )
    )
    movie_is_in_database = new_movie_name in movie_dict

    if not movie_is_in_database:
        movie_dict[new_movie_name] = {
            "rating": new_movie_rating,
            "release": new_movie_release,
        }
        print_colored_output(
            f'"✅ {new_movie_name} ({new_movie_release})" successfully added.', "green"
        )
    else:
        print_colored_output("❌ Movie is already in the database. Try again.", "red")


def delete_movie_from_database(movie_dict: dict[str, float]) -> None:
    """
    Deletes a movie from the database if it exists and gives feedback.

    :param movie_dict: Dictionary of movies and ratings.
    :return: None
    """
    movie_to_delete = get_colored_input(
        "Enter the name of the movie you want to delete: "
    )
    movie_is_in_database = movie_to_delete in movie_dict

    if movie_is_in_database:
        del movie_dict[movie_to_delete]
        print_colored_output(
            f'🗑️ "{movie_to_delete}" successfully deleted from the database.', "green"
        )
    else:
        print_colored_output("Movie is not in the database. Try again.", "red")


def update_movie_in_database(movie_dict: dict[str, dict]) -> None:
    movie_name = get_movie_from_database(movie_dict)
    try:
        new_rating = get_valid_movie_rating()
        movie_dict[movie_name]["rating"] = new_rating
        print_colored_output(f'✅ "{movie_name}" updated!', "green")
    except ValueError:
        pass  # Fehlerausgabe erfolgt bereits in get_valid_movie_rating
