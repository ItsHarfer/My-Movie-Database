"""
menu.py

Provides the menu logic for the  application.

This module is responsible for:
- Displaying available menu options based on the dispatcher
- Executing user-selected operations
- Managing the main menu loop

It connects user input to the corresponding handler functions defined in the dispatcher,
allowing interaction with the movie dataset via the command-line interface.

Author: Martin Haferanke
Date: 06.06.2025
"""

from config.config import (
    MENU_MIN_INDEX,
    MENU_MAX_INDEX,
    COLOR_MENU_OPTIONS,
    COLOR_ERROR,
    COMMANDS_REQUIRING_MOVIES,
)
from menu.menu_dispatcher import MOVIE_COMMAND_DISPATCHER
from helpers import get_input_by_type_and_range, get_colored_input
from printers import print_title, print_colored_output


def execute_operation(
    user_input: int, movie_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Executes the selected command from the user by invoking the corresponding handler.

    :param user_input: Integer representing the selected menu index.
    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    command_data = MOVIE_COMMAND_DISPATCHER.get(user_input)

    if not command_data:
        return print_colored_output(
            f"Unknown command '{user_input}'. Please select a valid option.",
            COLOR_ERROR,
        )

    if user_input in COMMANDS_REQUIRING_MOVIES and not movie_dict:
        return print_colored_output(
            "❌ No movies available. Can't execute operation.", COLOR_ERROR
        )

    return command_data["handler"](None, movie_dict)


def show_menu_options() -> None:
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


def run_menu_loop(movie_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Runs the interactive menu loop, allowing the user to select and execute commands.

    This loop:
    - Displays menu options
    - Prompts the user for a selection
    - Executes the corresponding operation
    - Waits for user confirmation to continue

    :param movie_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    while True:
        show_menu_options()
        user_choice = int(
            get_input_by_type_and_range(
                f"Enter command number ({MENU_MIN_INDEX}-{MENU_MAX_INDEX}): ",
                int,
                MENU_MIN_INDEX,
                MENU_MAX_INDEX,
            )
        )
        execute_operation(user_choice, movie_dict)
        get_colored_input("\nPress enter to continue...")
