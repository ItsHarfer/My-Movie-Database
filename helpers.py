import sys

from colorama import Style
from matplotlib import pyplot as plt

from config import COLOR_MAP
from printers import print_colored_output, print_movie


def quit_application():
    print("Bye!")
    sys.exit(0)


def get_colored_input(prompt: str, color: str = "light_magenta") -> str:
    """
    Prompts the user for input and output with colored text.

    :param prompt: Text shown to the user.
    :param color: Optional color name (default: 'light_magenta').
    :return: Trimmed user input as string.
    """
    color_prefix = COLOR_MAP.get(color, "")
    return input(color_prefix + prompt + Style.RESET_ALL).strip()


def search_movie(movie_dict: dict[str, dict]) -> None:
    """
    Searches for movies that contain a given string and displays matching results.

    :param movie_dict: Dictionary of movies and details.
    :return: None
    """
    search_query = get_colored_input("Enter part of movie name:").lower()
    matches = [
        (movie, details)
        for movie, details in movie_dict.items()
        if search_query in movie.lower()
    ]

    if matches:
        for movie, details in matches:
            print_movie(movie, details)
    else:
        print_colored_output("No search result.", "red")


def get_movies_sorted_by_rating(movie_dict: dict[str, float]) -> dict[str, float]:
    """
    Sorts the movies by their rating in descending order.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Dictionary of movies sorted by rating from highest to lowest.
    """
    sort_by_rating = lambda movie_item: movie_item[1]
    sorted_movie_dict = dict(
        sorted(movie_dict.items(), key=sort_by_rating, reverse=True)
    )
    return sorted_movie_dict


def get_rating_histogram(movie_dict: dict[str, float]) -> None:
    """
    Creates and saves a horizontal bar chart of movie ratings.

    :param movie_dict: Dictionary of movies and ratings.
    :return: None (but a .png file is saved).
    """
    file_name = get_colored_input("Please name your histogram (e.g.: ratings.png): ")
    if not file_name.endswith(".png"):
        file_name += ".png"

    movie_names_list = list(movie_dict.keys())
    movie_rating_list = list(movie_dict.values())

    plt.barh(movie_names_list, movie_rating_list)  # horizontal bar diagram

    plt.xlabel("Rating")
    plt.ylabel("Movie")
    plt.title("X-Rating")

    plt.tight_layout()
    plt.savefig(file_name)
    print_colored_output(f'Horizontal bar diagram saved in "{file_name}"', "green")


def get_colored_numeric_input_float(
    prompt: str, start_range: int, end_range: int
) -> float:
    while True:
        user_input = get_colored_input(prompt)
        try:
            number = float(user_input)
            if start_range <= number <= end_range:
                return number
            print_colored_output(
                f"Please enter a number between {start_range} and {end_range}.", "red"
            )
        except ValueError:
            print_colored_output("Please provide a valid number.", "red")
