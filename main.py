"""
main.py

Main entry point of the Movie Database application (SQL/HTML/API Edition).

This script launches an interactive command-line interface that allows users to
manage a personal collection of movies using an SQL-backed storage system.
Users can view, add, update, delete, and analyze movies, manage multiple profiles,
and export favorite movies as an HTML website.

Features:
- User management and session handling via `users.menu` and `users.session_user`
- Menu-driven interface using `run_movie_menu_loop` from `movie.menu`
- SQL-backed movie storage with `movie.storage_sql`
- Rich interactions supported by helper modules (`helpers.*`, `printers`, `analysis`)
- Filter, sort, and analyze movies with visualization and data exploration
- Generate HTML previews for personal movie collections

Required modules:
- movie.storage_sql: Handles all movie-related SQL database operations
- users.menu, users.session_user: User menu navigation and session control
- movie.menu: Main movie interaction menu
- printers: Formatted CLI output
- helpers.*: Input validation, HTML generation, filtering utilities
- analysis: Statistical analysis and matplotlib-based visualization

Author: Martin Haferanke
Date: 16.06.2025
"""

from movie.menu import run_movie_menu_loop
from movie import storage_sql

from printers import print_title
from users.menu import run_user_menu_loop
from users.session_user import get_active_user_id

active_user = None


def main() -> None:
    while True:
        print_title("My movie database - SQL Edition")
        run_user_menu_loop()
        user_id = get_active_user_id()
        movie_dict = storage_sql.list_movies(user_id)
        run_movie_menu_loop(movie_dict)


if __name__ == "__main__":
    main()
