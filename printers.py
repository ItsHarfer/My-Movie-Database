from colorama import Style

from config import ASTERISK_COUNT, COLOR_MAP, RATING_LIMIT, MENU_OPTIONS
from analysis import (
    get_calculated_average_rate,
    get_calculated_median_rate,
    get_all_movies_extremes_by_mode,
)


def print_title(title_name: str, star_count: int) -> None:
    """
    Prints a formatted title surrounded by a given number of asterisks on each side.

    :param title_name: The title text to display.
    :param star_count: Number of asterisks before and after the title.
    :return: None
    """
    print_ten_asterix = f"*" * star_count
    print_colored_output(
        "\n" + print_ten_asterix + f" {title_name} " + print_ten_asterix, "light_yellow"
    )


def print_movies_in_database(movie_dict: dict[str, float]) -> None:
    """
    Displays the total number of movies and prints each movie with its rating.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: None
    """
    total_movie_count = len(movie_dict)
    print_colored_output(f"\n{total_movie_count} ", "light_yellow", end="")
    print_colored_output("movies in total", "green")
    print_multiple_movies(movie_dict)


def print_menu_options() -> None:
    """
    Displays the main menu options for user interaction.

    :return: None
    """
    print_title("Menu", ASTERISK_COUNT)
    for index, option in enumerate(MENU_OPTIONS, start=0):
        print(f"{index} - ", end="")
        print_colored_output(f"{option}", "light_blue")
    print()


def print_colored_output(prompt: str, color: str = "cyan", end: str = "\n") -> None:
    """
    Prints the given text in the specified color using ANSI escape codes via colorama.

    :param prompt: The text to be displayed.
    :param color: The name of the color (default: 'cyan').
    :param end: End character for the print statement (default: new line).
    :return: None
    """
    color_prefix = COLOR_MAP.get(color, "")
    print(color_prefix + prompt + Style.RESET_ALL, end=end)


def print_movies_statistics_in_database(movie_dict: dict[str, float]) -> None:
    """
    Calculates and displays statistics about the movies in the database,
    including average rating, median rating, best and worst movies.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: None
    """
    average_rate = get_calculated_average_rate(movie_dict)
    median_rate = get_calculated_median_rate(movie_dict)
    try:
        best_movies = get_all_movies_extremes_by_mode(movie_dict, "best")
        worst_movies = get_all_movies_extremes_by_mode(movie_dict, "worst")
    except ValueError as e:
        print_colored_output(str(e), "red")
        return

    print_title("Movie Statistics", 3)
    print_colored_output(f"Average rating: ", "blue", end="")
    print_colored_output(f"{average_rate}", "light_yellow")

    print_colored_output(f"Median rating: ", "blue", end="")
    print_colored_output(f"{median_rate}", "light_yellow")

    print_colored_output(f"Best movie(s): ", "blue")
    print_multiple_movies(best_movies)

    print_colored_output(f"Worst movie(s): ", "blue")
    print_multiple_movies(worst_movies)


def print_random_movie(name: str, rating: float) -> None:
    """
    Displays a randomly selected movie and its rating.

    :param name: The title of the randomly selected movie.
    :param rating: The rating of the selected movie.
    :return: None
    """
    print_colored_output(f"Your movie for tonight: ", "light_blue")
    print_colored_output(f"- {name}: ", end="")
    print_colored_output(f"{rating}", "light_yellow")


def print_movie(movie_title: str, movie_details: dict) -> None:
    """
    Prints the title and rating of a single movie in a formatted and colored output.

    :param movie_title: The name of the movie.
    :param movie_details:
    :return: None
    """
    movie_rating = movie_details["rating"]
    movie_release = movie_details["release"]
    print_colored_output(f"- {movie_title} ({movie_release}): ", "light_blue", end="")
    print_colored_output(f" Rating: {movie_rating}/{RATING_LIMIT}", "light_yellow")


def print_multiple_movies(movie_dict: dict) -> None:
    """
    Prints all movies and their ratings from the given dictionary.

    :param movie_dict:
    :param movie_list: List of movie titles, ratings and release years.

    """
    for movie_title, movie_details in movie_dict.items():
        print_colored_output(
            movie_title + f" ({movie_details["release"]})", "yellow", end=""
        )
        print(f" Rating: {movie_details["rating"]}")
    print()
