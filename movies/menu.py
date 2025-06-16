"""
menu / menu.py

Provides the menu logic for the Movie Database application.

This module is responsible for:
- Displaying available menu options using the dispatcher
- Executing user-selected operations based on input
- Managing the main menu loop and session lifecycle
- Dynamically greeting users by name
- Exiting the menu loop if no user is logged in

It connects user input to the corresponding handler functions defined in the dispatcher,
enabling interaction with the movies dataset via the command-line interface.

Author: Martin Haferanke
Date: 13.06.2025
"""

from config.config import (
    MENU_MIN_INDEX,
    MENU_MAX_INDEX,
    COLOR_MENU_OPTIONS,
    COLOR_SUCCESS,
)
from helpers.dispatcher_utils import execute_operation
from helpers.input_utils import get_input_by_type_and_range, get_colored_input
from movies.dispatcher import MOVIE_COMMAND_DISPATCHER
from printers import print_title, print_colored_output
from users import session_user
from users.session_user import get_active_user_id


def show_movie_menu_options() -> None:
    """
    Displays the main menu options using the command dispatcher labels.

    :return: None
    """
    print_title("Menu")
    for index in sorted(MOVIE_COMMAND_DISPATCHER):
        label = MOVIE_COMMAND_DISPATCHER[index]["label"]
        print(f"{index} - ", end="")
        print_colored_output(label, COLOR_MENU_OPTIONS)
    print()


def run_movie_menu_loop(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Runs the interactive menu loop, allowing the user to select and execute commands.

    This loop:
    - Displays menu options
    - Prompts the user for a selection
    - Executes the corresponding operation
    - Waits for user confirmation to continue

    :param movie_dict: Dictionary of movies titles and their attribute dictionaries.
    :return: None
    """

    while True:
        print()
        print_colored_output(
            f"🎬 Hey {session_user.get_active_user()}, welcome back!\n", COLOR_SUCCESS
        )
        show_movie_menu_options()
        user_choice = int(
            get_input_by_type_and_range(
                f"Enter command number ({MENU_MIN_INDEX}-{MENU_MAX_INDEX}): ",
                int,
                MENU_MIN_INDEX,
                MENU_MAX_INDEX,
            )
        )
        execute_operation(user_choice, movie_dict, MOVIE_COMMAND_DISPATCHER)

        get_colored_input("\nPress enter to continue...")

        # Exit loop if the user is not logged in
        if not get_active_user_id():
            break
