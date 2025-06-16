"""
helpers / movie_utils.py

Provides utility functions for extracting, parsing, and validating movie-related data structures.

This module supports attribute extraction from movie dictionaries, country name conversion to ISO codes,
and parsing of structured field data for validation and transformation purposes.

Functions:
- extract_country_codes: Converts comma-separated country names into ISO alpha-2 codes.
- extract_valid_attributes: Retrieves attribute names from the first valid movie dictionary entry.
- parse_fields: Extracts and casts specific fields from a data dictionary with type validation.

These helpers are commonly used to sanitize and prepare movie data for display, storage, or API consumption.

Author: Martin Haferanke
Date: 16.06.2025
"""

from config.config import COLOR_ERROR, COUNTRY_NAME_TO_CODE
from printers import print_colored_output


def extract_country_codes(country_string: str) -> list[str]:
    """
    Converts a string of comma-separated country names into a list of ISO alpha-2 codes.

    :param country_string: Comma-separated country names (e.g. "United States, Canada").
    :return: List of valid ISO alpha-2 codes (e.g. ['US', 'CA']).
    """
    return [
        COUNTRY_NAME_TO_CODE.get(country.strip())
        for country in country_string.split(",")
        if COUNTRY_NAME_TO_CODE.get(country.strip())
    ]


def extract_valid_attributes(movie_dict: dict[str, dict]) -> set[str]:
    """
    Extracts a set of valid attribute names from the first movie entry in the dictionary.

    Returns an empty set if the dictionary is empty or invalid.

    :param movie_dict: Dictionary of movie titles and their attributes.
    :return: Set of attribute names.
    """
    if not movie_dict:
        print_colored_output("❌ No movies available with attributes.", COLOR_ERROR)
        return set()

    for attributes in movie_dict.values():
        if isinstance(attributes, dict):
            return set(attributes.keys())
    return set()


def parse_fields(data: dict, required_fields: dict[str, type]) -> dict:
    """
    Extracts and converts specified fields from a data dictionary.

    :param data: The source dictionary (e.g., API response).
    :param required_fields: A dict where keys are field names to extract
                            and values are the expected Python types (e.g., float, int, str).
    :return: A dict with the extracted and converted fields.
    :raises ValueError: if a field is missing or cannot be converted.
    """
    result = {}
    for field, expected_type in required_fields.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        raw_value = data[field]
        try:
            result[field] = expected_type(raw_value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value for field '{field}': {raw_value}")
    return result
