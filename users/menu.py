"""
users / menu.py

Provides the user selection menu logic for the Movie Database application.

This module is responsible for:
- Displaying a sorted and numbered menu of existing users, followed by an option to create a new user.
- Allowing user selection from existing accounts or initiating the creation of a new user.
- Running a continuous loop until a valid user is selected or created successfully.

It integrates user input handling, dispatcher mapping, and command execution into a cohesive
menu-driven user management system.

Author: Martin Haferanke
Date: 13.06.2025
"""

from config.config import COLOR_MENU_OPTIONS
from helpers import get_input_by_type_and_range
from printers import print_title, print_colored_output
from users import storage_sql
from users.dispatcher import get_user_command_dispatcher


def show_user_menu_options() -> None:
    """
    Displays a sorted list of users from the dispatcher followed by a create-user option.

    - Sorts users alphabetically.
    - Numbers existing users starting from 1.
    - Adds 'Create new user' option at the end.

    :return: None
    """
    print_title("User Menu")
    dispatcher = get_user_command_dispatcher()

    # Separate all user entries except the "Create new user" option
    user_entries = [
        (key, value)
        for key, value in dispatcher.items()
        if value["label"] != "Create new user"
    ]

    # Find the "Create new user" entry, if it exists
    create_entry = next(
        (value for value in dispatcher.values() if value["label"] == "Create new user"),
        None,
    )

    # Sort the user entries alphabetically by their label (case-insensitive)
    user_entries.sort(key=get_label_lower)

    # Print each user entry with an index and user ID
    for index, (user_id, user_data) in enumerate(user_entries, start=1):
        label = f"{user_data['label']} (id:{user_id})"
        print_colored_output(f"{index}. {label}", COLOR_MENU_OPTIONS)

    # Print the "Create new user" option at the end, if it exists
    if create_entry:
        print_colored_output(
            f"{len(user_entries) + 1}. {create_entry['label']}", COLOR_MENU_OPTIONS
        )

    print()


def get_label_lower(entry):
    """
    Extracts the lowercase version of the label from a user entry tuple.

    This function is used as a key function for sorting user entries alphabetically
    in a case-insensitive manner.

    :param entry: A tuple of (user_id, user_data_dict), where user_data_dict contains a 'label'.
    :return: Lowercase string of the user's label for sorting purposes.
    """
    return entry[1]["label"].lower()


def run_user_menu_loop() -> None:
    """
    Executes the user selection menu loop.

    This function:
    - Displays the user selection menu.
    - Prompts for and processes user input.
    - Executes the selected command handler.
    - Continues until a user is selected or successfully created.

    :return: None
    """
    while True:
        user_dict = storage_sql.list_users()

        # Get the dispatcher mapping for user commands
        dispatcher = get_user_command_dispatcher()

        show_user_menu_options()

        user_menu_max_index = len(dispatcher)

        user_choice = int(
            get_input_by_type_and_range(
                f"Enter command number (1-{user_menu_max_index}): ",
                int,
                1,
                user_menu_max_index,
            )
        )

        # Prepare a sorted list of user entries excluding the 'Create new user' option
        sorted_dispatcher = [
            (k, v) for k, v in dispatcher.items() if v["label"] != "Create new user"
        ]
        sorted_dispatcher.sort(key=get_label_lower)

        if user_choice == len(sorted_dispatcher) + 1:
            # User selected the 'Create new user' option
            selected_command = next(
                (v for v in dispatcher.values() if v["label"] == "Create new user"),
                None,
            )
        else:
            # User selected an existing user
            selected_command = sorted_dispatcher[user_choice - 1][1]

        # Execute the selected command with required arguments
        executed = selected_command["handler"](
            None, user_dict, selected_command["args"]
        )

        # Exit the loop if a user was successfully selected or created
        if executed:
            break
