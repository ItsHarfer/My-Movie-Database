# =====================================================
# 🟢 CRUD Functions – Add, delete, update movies
# =====================================================
from random import Random

from helpers import get_colored_input, get_colored_numeric_input_float
from printers import print_colored_output


def get_random_movie(movie_dict: dict[str, float]) -> tuple[str, float]:
    """
    Selects a random movie from the database.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Tuple (movie_name, movie_rating).
    """
    movies_count_to_index = len(movie_dict) - 1
    movies_as_list = list(movie_dict.keys())

    random_number = Random().randint(0, movies_count_to_index)

    random_movie_name = movies_as_list[random_number]
    random_movie_rating = movie_dict[random_movie_name]
    return random_movie_name, random_movie_rating

def add_movie_to_database(movie_dict: dict[str, float]) -> None:
    """
    Adds a new movie with its rating to the movie dictionary.

    :param movie_dict: Dictionary of movies and their ratings.
    :return: None
    """
    new_movie_name = get_colored_input('Enter new movie name: ')
    new_movie_rating = get_colored_numeric_input_float('Enter new movie rating (0-10): ', 0, 10)
    movie_is_in_database = new_movie_name in movie_dict

    if not movie_is_in_database:
        movie_dict[new_movie_name] = new_movie_rating
        print_colored_output(f'"{new_movie_name}" successfully added.', 'green')
    else:
        print_colored_output('Movie is already in the database. Try again.', 'red')


def delete_movie_from_database(movie_dict: dict[str, float]) -> None:
    """
    Deletes a movie from the database if it exists and gives feedback.

    :param movie_dict: Dictionary of movies and ratings.
    :return: None
    """
    movie_to_delete = get_colored_input('Enter the name of the movie you want to delete: ')
    movie_is_in_database = movie_to_delete in movie_dict

    if movie_is_in_database:
        del movie_dict[movie_to_delete]
        print_colored_output(f'"{movie_to_delete}" successfully deleted from the database.', 'green')
    else:
        print_colored_output('Movie is not in the database. Try again.', 'red')


def update_movie_in_database(movie_dict: dict[str, float]) -> None:
    """
    Updates the rating of an existing movie in the database if the movie is found.

    :param movie_dict: Dictionary of movies and their ratings.
    :return: None
    """
    movie_is_updated = False
    while not movie_is_updated:
        movie_to_update = get_colored_input('Enter the name of the movie you want to update: ')
        movie_is_in_database = movie_to_update in movie_dict

        if movie_is_in_database:
            print_colored_output(f'"{movie_to_update}" found! ', 'green')
            update_movie_rating = get_colored_numeric_input_float('Enter the new rating for the movie: ', 0, 10)
            movie_dict[movie_to_update] = update_movie_rating
            print_colored_output(f'{movie_to_update} updated!', 'green')
            movie_is_updated = True

        else:
            print_colored_output('Movie not found. Please try again.', 'red')