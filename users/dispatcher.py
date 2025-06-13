"""
dispatcher.py

Provides user operation dispatcher logic for the Movie Database application.

This module is responsible for:
- Creating a dispatcher dictionary mapping user IDs to handler functions and labels.
- Providing an option for creating a new user.
- Enabling dynamic interaction by linking user selections to corresponding handlers.

It supports the menu-driven user interaction model, ensuring clear and organized
execution of user-related operations.

Author: Martin Haferanke
Date: 13.06.2025
"""

# Dispatcher mapping for user operations
from users import storage_sql
from users.handler import handle_create_user, handle_select_user


def get_user_command_dispatcher():
    """
    Creates a dispatcher dictionary for available user options and user creation.

    This dispatcher maps:
    - Existing user IDs to their selection handlers.
    - A dedicated option for creating new users.

    Each dispatcher entry includes:
    - 'handler': function reference for handling selection or creation.
    - 'label': descriptive text (e.g., username or action label).
    - 'args': arguments passed to the handler function.

    :return: Dispatcher dictionary structured for user selection and creation.
    """
    users = storage_sql.list_users()
    dispatcher = {}

    for user_id, user_data in users.items():
        dispatcher[user_id] = {
            "handler": handle_select_user,
            "label": f"{user_data['username']}",
            "args": user_id,
        }

    dispatcher[len(users) + 1] = {
        "handler": handle_create_user,
        "label": "Create new user",
        "args": None,
    }

    return dispatcher


USER_COMMAND_DISPATCHER = get_user_command_dispatcher()
