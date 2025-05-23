import json


def get_data_from_file(filename: str) -> dict[str, dict[str, float | int]]:
    """
    Loads and returns structured movie (or ship) data from a JSON file.

    Expects the file to contain a dictionary of string keys mapping to dictionaries
    with numeric attributes like ratings or release years.

    :param filename: Path to the JSON file to be loaded.
    :return: Dictionary of items, each containing attribute dictionaries with float or int values.
    """
    with open(filename, "r") as file:
        all_data = json.load(file)
    return dict(all_data)


def save_movies(movie_dict: dict[str, dict[str, float | int]], filename: str) -> None:
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(filename, "w") as file:
        json.dump(movie_dict, file, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    pass


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    pass


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    pass
