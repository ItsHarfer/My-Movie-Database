"""
session_user.py

Manages the currently active user in the Movie Database application.

This module provides helper functions to set, retrieve, and clear the active user,
as well as to validate if a user is currently selected before performing actions.

Author: Martin Haferanke
Date: 13.06.2025
"""

from config.config import COLOR_ERROR
from printers import print_colored_output

active_user = None
active_user_id = None


def set_active_user(user_id: int, username: str) -> None:
    """
    Sets the currently active user.

    :param user_id: The ID of the user to set as active.
    :param username: The username of the user to set as active.
    :return: None
    """
    global active_user, active_user_id
    active_user = username
    active_user_id = user_id


def get_active_user_id() -> int | None:
    """
    Returns the ID of the currently active user.

    :return: User ID if available, otherwise None.
    """
    return active_user_id


def get_active_user() -> str | None:
    """
    Returns the username of the currently active user.

    :return: Username if available, otherwise None.
    """
    return active_user


def clear_active_user() -> None:
    """
    Clears the currently active user information.

    :return: None
    """
    global active_user, active_user_id
    active_user = None
    active_user_id = None


def abort_if_no_active_user() -> int | None:
    """
    Checks whether an active user is set; aborts with an error message if not.

    :return: The active user's ID if available, otherwise None.
    """
    user_id = get_active_user_id()
    if user_id is None:
        print_colored_output(
            "❌ No active user! Please select a user first.", COLOR_ERROR
        )
        return None
    return user_id
