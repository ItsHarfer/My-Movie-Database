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


def print_movies_in_database(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Displays the total number of movies and prints each movie with its rating.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: None
    """
    total_movie_count = len(movie_dict)
    print_colored_output(f"\n{total_movie_count} ", "light_yellow", end="")
    print_colored_output("movies in total", "green")
    print_movies(movie_dict)


def print_menu_options() -> None:
    """
    Displays the main menu options for user interaction.

    :return: None
    """
    print_title("Menu", ASTERISK_COUNT)
    for index, option in enumerate(MENU_OPTIONS):
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


def print_movies_statistics_in_database(
    movie_dict: dict[str, dict[str, float | int]],
) -> None:
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
    print_colored_output(f"{average_rate:.2f}", "light_yellow")

    print_colored_output(f"Median rating: ", "blue", end="")
    print_colored_output(f"{median_rate:.2f}", "light_yellow")

    print_colored_output(f"Best movie(s): ", "blue")
    print_movies(best_movies)

    print_colored_output(f"Worst movie(s): ", "blue")
    print_movies(worst_movies)


def print_movies(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Prints movie(s) and their ratings from the given dictionary.

    :param movie_dict: Dictionary of movie titles and their details.
    """
    for title, details in movie_dict.items():
        rating = details["rating"]
        release = details["release"]
        print_colored_output(f"- {title} ({release}): ", "light_blue", end="")
        print_colored_output(f"Rating: {rating}/{RATING_LIMIT}", "light_yellow")
