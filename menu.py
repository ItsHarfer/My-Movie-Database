"""
menu.py


"""

from handlers import MOVIE_COMMAND_DISPATCHER
from helpers import get_colored_numeric_input_float, get_colored_input
from printers import print_menu_options


def is_available_command(user_input: str) -> bool:
    """
    Check if the given user input is a valid command.

    :param user_input: The command entered by the user.
    :type user_input: str
    :return: True if the command is available, False otherwise.
    :rtype: bool
    """
    return user_input in MOVIE_COMMAND_DISPATCHER


def execute_operation(user_input: int, movies_data: list[dict]) -> None:
    """
    Executes the selected command from the user.
    """
    command_data = MOVIE_COMMAND_DISPATCHER.get(user_input)
    if command_data:
        command_data["handler"](None, movies_data)
    else:
        print(f"Unknown command '{user_input}'. Please select a valid option.")


def run_menu_loop(movies_data) -> None:
    """ """
    while True:
        print_menu_options()
        user_choice = int(
            get_colored_numeric_input_float("Enter new movie rating (0-9): ", 0, 9)
        )
        execute_operation(user_choice, movies_data)
        get_colored_input("\nPress enter to continue...")
