"""
helpers / dispatcher_utils.py

Executes user-selected commands based on a dispatcher mapping of menu indices to handlers.

This module handles routing of CLI menu selections to their corresponding function handlers.
It supports modular command execution by decoupling input handling from action logic.

Functions:
- execute_operation: Executes the handler associated with a menu option from the dispatcher mapping.

This promotes separation of concerns and simplifies extension or modification of application behavior.

Author: Martin Haferanke
Date: 16.06.2025
"""

from config.config import COLOR_ERROR
from printers import print_colored_output


def execute_operation(user_input: int, data: dict, dispatcher: dict[int, dict]) -> bool:
    """
    Executes the selected command from the user by invoking the corresponding handler out from the dispatcher.

    :param user_input: Index of the selected menu command.
    :param data: Context data passed to the handler (e.g., user or movies data).
    :param dispatcher: Mapping of menu indices to command handler definitions.
    :return: True if the handler was successfully executed, False otherwise.
    """
    command_data = dispatcher.get(user_input)
    if not command_data:
        print_colored_output(
            f"Unknown command '{user_input}'. Please select a valid option.",
            COLOR_ERROR,
        )
        return False

    args = command_data.get("args", [])
    result = command_data["handler"](None, data, args)

    return bool(result)
