"""
menu_dispatcher.py

Centralized command dispatcher for the Movie Database application.

This module defines the mapping between numerical menu commands and their
corresponding handler functions and descriptions.

The `MOVIE_COMMAND_DISPATCHER` dictionary enables the main menu loop to dynamically
route user input to the appropriate functionality, providing a clean and extensible
architecture for command handling.

Each command is associated with:
- a numeric identifier (as displayed in the CLI menu)
- a callable function (from the handlers module)
- a user-facing description label

Author: Martin Haferanke
Date: 06.06.2025
"""

from menu_handlers import (
    handle_quit_application,
    handle_show_movies,
    handle_add_movie,
    handle_delete_movie,
    handle_update_movie,
    handle_show_movie_statistics,
    handle_random_movie,
    handle_search_movie,
    handle_sorted_movies_by_attribute,
    handle_create_histogram_by_attribute,
    handle_filter_movies,
    handle_generate_website,
)

# Dispatcher mapping for movie operations
MOVIE_COMMAND_DISPATCHER = {
    0: {
        "handler": handle_quit_application,
        "label": "Quit application",
    },
    1: {
        "handler": handle_show_movies,
        "label": "List movies",
    },
    2: {
        "handler": handle_add_movie,
        "label": "Add movie",
    },
    3: {
        "handler": handle_delete_movie,
        "label": "Delete movie",
    },
    4: {
        "handler": handle_update_movie,
        "label": "Update movie",
    },
    5: {
        "handler": handle_show_movie_statistics,
        "label": "Stats",
    },
    6: {
        "handler": handle_random_movie,
        "label": "Random movie",
    },
    7: {
        "handler": handle_search_movie,
        "label": "Search movie",
    },
    8: {
        "handler": handle_sorted_movies_by_attribute,
        "label": "Movies sorted by an attribute you choose",
    },
    9: {
        "handler": handle_create_histogram_by_attribute,
        "label": "Create Rating Histogram",
    },
    10: {
        "handler": handle_filter_movies,
        "label": "Show only movies matching your rating and year criteria",
    },
    11: {
        "handler": handle_generate_website,
        "label": "Generate website for your favorite movies.",
    },
}
