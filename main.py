"""
main.py

Main entry point of the Movie Database application (SQL/HTML/API Edition).

This script launches an interactive command-line interface that allows users to
manage a personal collection of movies using an SQL-backed storage system.
Users can view, add, update, delete, and analyze movies, manage multiple profiles,
and export favorite movies as an HTML website.

Features:
- User management and session handling via `users.menu` and `users.session_user`
- Menu-driven interface using `run_movie_menu_loop` from `movies.menu`
- SQL-backed movies storage with `movies.storage_sql`
- Rich interactions supported by helper modules (`helpers.*`, `printers`, `analysis`)
- Filter, sort, and analyze movies with visualization and data exploration
- Generate HTML previews for personal movies collections

Required modules:
- movies.storage_sql: Handles all movies-related SQL database operations
- users.menu, users.session_user: User menu navigation and session control
- movies.menu: Main movies interaction menu
- printers: Formatted CLI output
- helpers.*: Input validation, HTML generation, filtering utilities
- analysis: Statistical analysis and matplotlib-based visualization

Author: Martin Haferanke
Date: 16.06.2025
"""

from movies.menu import run_movie_menu_loop
from movies import storage_sql

from printers import print_title
from users.menu import run_user_menu_loop
from users.session_user import get_active_user_id

active_user = None


def main() -> None:
    while True:
        print_title("My movies database - SQL Edition")
        run_user_menu_loop()
        user_id = get_active_user_id()
        movie_dict = storage_sql.list_movies(user_id)
        run_movie_menu_loop(movie_dict)


if __name__ == "__main__":
    main()
