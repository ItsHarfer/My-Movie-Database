"""
dispatcher.py

Centralized command dispatcher for the Movie Database application.

This module defines the mapping between numerical menu commands and their
corresponding handler functions and descriptions.

The `MOVIE_COMMAND_DISPATCHER` dictionary enables the main menu loop to dynamically
route user input to the appropriate functionality, providing a clean and extensible
architecture for command handling.

Each command is associated with:
- a numeric identifier (as displayed in the CLI menu)
- a callable function (from the handlers module or user handler)
- a user-facing description label

Available Commands:
0  - Quit application
1  - List movies
2  - Add movie
3  - Delete movie
4  - Update movie
5  - Stats
6  - Random movie
7  - Search movie
8  - Movies sorted by an attribute you choose
9  - Create Rating Histogram
10  - Show only movies matching your rating and year criteria
11  - Generate website for your favorite movies
12  - Switch user

Author: Martin Haferanke
Date: 06.06.2025
"""

from menu.handlers import (
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
from users.handler import handle_switch_user

# Dispatcher mapping for movie operations
MOVIE_COMMAND_DISPATCHER = {
    0: {
        "handler": handle_quit_application,
        "label": "Quit application",
        "args": None,
    },
    1: {
        "handler": handle_show_movies,
        "label": "List movies",
        "args": None,
    },
    2: {
        "handler": handle_add_movie,
        "label": "Add movie",
        "args": None,
    },
    3: {
        "handler": handle_delete_movie,
        "label": "Delete movie",
        "args": None,
    },
    4: {
        "handler": handle_update_movie,
        "label": "Update movie",
        "args": None,
    },
    5: {
        "handler": handle_show_movie_statistics,
        "label": "Stats",
        "args": None,
    },
    6: {
        "handler": handle_random_movie,
        "label": "Random movie",
        "args": None,
    },
    7: {
        "handler": handle_search_movie,
        "label": "Search movie",
        "args": None,
    },
    8: {
        "handler": handle_sorted_movies_by_attribute,
        "label": "Movies sorted by an attribute you choose",
        "args": None,
    },
    9: {
        "handler": handle_create_histogram_by_attribute,
        "label": "Create Rating Histogram",
        "args": None,
    },
    10: {
        "handler": handle_filter_movies,
        "label": "Show only movies matching your rating and year criteria",
        "args": None,
    },
    11: {
        "handler": handle_generate_website,
        "label": "Generate website for your favorite movies.",
        "args": None,
    },
    12: {
        "handler": handle_switch_user,
        "label": "Switch user",
        "args": None,
    },
}
