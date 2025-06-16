"""
helpers / input_utils.py

Provides helper functions for collecting and validating user input with colored CLI prompts.

This module ensures consistent and user-friendly input collection across the application.
It supports type validation, value range checks, option restriction, and customizable color prompts.
Color formatting is applied using the colorama library and centralized configuration values.

Functions:
- get_colored_input: Prompts user with colored input text and returns the trimmed result.
- get_type_validated_input: Ensures input matches an expected Python type.
- get_content_validated_input: Validates input against a predefined set of allowed strings.
- get_input_by_type_and_range: Validates an input type and ensures it's within a specified numeric range.
- get_current_year: Returns the current calendar year.

These utilities help enforce robust and consistent input validation throughout the CLI application.

Author: Martin Haferanke
Date: 16.06.2025
"""

from datetime import datetime
from colorama import Style

from config.config import COLOR_ERROR, COLOR_MAP, COLOR_INPUT
from printers import print_colored_output


def get_colored_input(prompt: str, color: str = COLOR_INPUT) -> str:
    """
    Prompts the user for input and output with colored text.

    :param prompt: Text shown to the user.
    :param color: Optional color name (default: 'light_magenta').
    :return: Trimmed user input as string.
    """
    color_prefix = COLOR_MAP.get(color, "")
    return input(color_prefix + prompt + Style.RESET_ALL).strip()


def get_type_validated_input(prompt: str, expected_type: type) -> int | float | str:
    """
    Prompts the user for input and converts it to the expected type.

    Repeats until the input can be converted to the given data type (e.g., int, float, str).
    Displays an error message for invalid conversions.

    :param prompt: Text shown to the user.
    :param expected_type: The expected Python type.
    :return: The input value converted to the expected type.
    """
    while True:
        user_input = get_colored_input(prompt)
        try:
            return expected_type(user_input)
        except ValueError:
            print_colored_output(
                f"❌ Invalid input. Please enter a valid {expected_type.__name__}.",
                COLOR_ERROR,
            )


def get_content_validated_input(prompt: str, valid_options: set[str]) -> str:
    """
    Prompts the user for input and validates it against a set of allowed options.

    The input is displayed in color and repeated until a valid value is entered.

    :param prompt: The text to display to the user.
    :param valid_options: A set of accepted string values.
    :return: A validated and normalized user input string.
    """
    while True:
        user_input = get_colored_input(prompt)
        if user_input in valid_options:
            return user_input
        print_colored_output(
            f"❌ Invalid input '{user_input}'. Please enter one of: {', '.join(valid_options)}.",
            COLOR_ERROR,
        )


def get_input_by_type_and_range(
    prompt: str,
    datatype: type,
    start_range: float,
    end_range: float,
    valid_empty_input=False,
) -> float | None:
    """
    Prompts the user to enter a floating-point number within a specified range.
    The input is validated, and an error message is shown if the input is invalid
    or out of range.

    :param valid_empty_input: If True, allows an empty string input and returns None.
    :param datatype: The datatype to cast for
    :param prompt: The message is shown to the user.
    :param start_range: The minimum acceptable value (inclusive).
    :param end_range: The maximum acceptable value (inclusive).
    :return: A validated number of the specified type or None (if empty input is allowed).
    """
    while True:
        user_input = get_colored_input(prompt)
        if valid_empty_input and user_input == "":
            return None
        try:
            user_input_with_type = datatype(user_input)
            if start_range <= user_input_with_type <= end_range:
                return user_input_with_type
            else:
                print_colored_output(
                    f"❌ Please enter a value between {start_range} and {end_range}.",
                    COLOR_ERROR,
                )
        except ValueError:
            print_colored_output(
                "❌ Invalid input. Please enter a valid number.", COLOR_ERROR
            )


def get_current_year() -> int:
    """
    Returns the current calendar year as a four-digit integer.

    Uses the system's current date and time to extract the year.

    :return: The current year
    """
    return datetime.now().year
