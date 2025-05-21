"""
menu.py


"""

from config import MENU_MIN_INDEX, MENU_MAX_INDEX
from handlers import MOVIE_COMMAND_DISPATCHER
from helpers import get_colored_numeric_input_float, get_colored_input
from printers import print_menu_options


def execute_operation(
    user_input: int, movies_dict: dict[str, dict[str, float | int]]
) -> None:
    """
    Executes the selected command from the user.
    """
    command_data = MOVIE_COMMAND_DISPATCHER.get(user_input)

    if command_data:
        command_data["handler"](None, movies_dict)
    else:
        print(f"Unknown command '{user_input}'. Please select a valid option.")


def run_menu_loop(movies_dict: dict[str, dict[str, float | int]]) -> None:
    """ """
    while True:
        print_menu_options()
        user_choice = int(
            get_colored_numeric_input_float(
                f"Enter new movie rating ({MENU_MIN_INDEX}-{MENU_MAX_INDEX}): ",
                MENU_MIN_INDEX,
                MENU_MAX_INDEX,
            )
        )
        execute_operation(user_choice, movies_dict)
        get_colored_input("\nPress enter to continue...")
