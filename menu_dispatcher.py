from handlers import (
    handle_quit_application,
    handle_show_movies,
    handle_add_movie,
    handle_delete_movie,
    handle_update_movie,
    handle_show_movie_statistics,
    handle_random_movie,
    handle_search_movie,
    handle_sorted_movies_by_rating,
    handle_create_histogram_by_attribute,
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
        "handler": handle_sorted_movies_by_rating,
        "label": "Movies sorted by rating",
    },
    9: {
        "handler": handle_create_histogram_by_attribute,
        "label": "Create Rating Histogram",
    },
}
