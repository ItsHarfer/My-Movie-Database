"""
main.py

Main entry point of the Movie Database application (SQL Edition).

This script launches an interactive command-line interface that allows users to
manage a collection of movies using an SQL-backed storage system. Users can view,
add, update, and delete movies, as well as analyze data through built-in statistics
and visualization features.

Features:
- Menu-driven interface using `run_menu_loop` from `menu.py`
- Loads and modifies movie data via `movie_storage_sql.py`
- Supports rich interaction through helper and handler modules
- Displays statistics on movie ratings, release years, and trends
- Integrates HTML generation for website previews of the movie database

Required modules:
- movie_storage_sql.py: Handles SQL database interactions
- menu.py, menu_dispatcher.py: Menu definitions and logic
- printers.py: Console output formatting
- menu_handlers.py, helpers.py: Input handling, filtering, validation, and HTML rendering
- analysis.py: Visualization and analysis tools

Author: Martin Haferanke
Date: 06.06.2025
"""

from movie_storage import movie_storage_sql
from menu.menu import run_menu_loop
from printers import print_title


def main() -> None:
    print_title("My movie database - SQL Edition")
    movie_dict = movie_storage_sql.list_movies()
    run_menu_loop(movie_dict)


if __name__ == "__main__":
    main()
