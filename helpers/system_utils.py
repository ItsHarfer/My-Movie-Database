"""
helpers / system_utils.py

Provides system-level utility functions for application control.

This module includes helper functions to manage system-related operations such as
cleanly exiting the application with user feedback.

Functions:
- quit_application: Prints a farewell message and exits the program with status code 0.

Useful for centralizing program termination logic and maintaining consistent behavior on exit.

Author: Martin Haferanke
Date: 16.06.2025
"""

import sys


def quit_application() -> None:
    """
    Exits the application.

    Prints a farewell message to the console and then terminates the program
    with a status code of 0 (successful exit).
    :return: None
    """
    print("Bye!")
    sys.exit(0)
