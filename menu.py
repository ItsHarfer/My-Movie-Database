"""
menu.py

Provides the menu logic for the  application.

This module is responsible for:
- Displaying available menu options based on the dispatcher
- Executing user-selected operations
- Managing the main menu loop

It connects user input to the corresponding handler functions defined in the dispatcher,
allowing interaction with the movie dataset via the command-line interface.
"""

from config import MENU_MIN_INDEX, MENU_MAX_INDEX, ASTERISK_COUNT, COLOR_MENU_OPTIONS
from menu_dispatcher import MOVIE_COMMAND_DISPATCHER
from helpers import get_input_by_type_and_range, get_colored_input
from printers import print_title, print_colored_output


def execute_operation(
    user_input: int, movies_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Executes the selected command from the user by invoking the corresponding handler.

    :param user_input: Integer representing the selected menu index.
    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    command_data = MOVIE_COMMAND_DISPATCHER.get(user_input)

    if command_data:
        command_data["handler"](
            None, movies_dict
        )  # None here for now, maybe later adding some parameters from the user input
    else:
        print(f"Unknown command '{user_input}'. Please select a valid option.")


def print_menu_options() -> None:
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


def run_menu_loop(movies_dict: dict[str, dict[str, float | int]]) -> None:
    """
    Runs the interactive menu loop, allowing the user to select and execute commands.

    This loop:
    - Displays menu options
    - Prompts the user for a selection
    - Executes the corresponding operation
    - Waits for user confirmation to continue

    :param movies_dict: Dictionary of movie titles and their attribute dictionaries.
    :return: None
    """
    while True:
        print_menu_options()
        user_choice = int(
            get_input_by_type_and_range(
                f"Enter command number ({MENU_MIN_INDEX}-{MENU_MAX_INDEX}): ",
                int,
                MENU_MIN_INDEX,
                MENU_MAX_INDEX,
            )
        )
        execute_operation(user_choice, movies_dict)
        get_colored_input("\nPress enter to continue...")
