"""
main.py

Main entry point of the Movie Database application (SQL/HMTL/API Edition).

This script launches an interactive command-line interface that allows users to
manage a collection of movies using an SQL-backed storage system. Users can view,
add, update, and delete movies, analyze data, and manage multiple user profiles.

Features:
- User management and login using `users.menu` and `users.users`
- Menu-driven interface using `run_menu_loop` from `menu.menu`
- Loads and modifies movie data via `movie_storage.storage_sql`
- Supports rich interaction through helper and handler modules
- Displays statistics on movie ratings, release years, and trends
- Integrates HTML generation for website previews of the movie database

Required modules:
- movie_storage.storage_sql: Handles SQL database interactions
- users.menu, users.users: User selection and active user state
- menu.menu, menu.dispatcher: Menu definitions and logic
- printers: Console output formatting
- menu.handlers, helpers: Input handling, filtering, validation, and HTML rendering
- analysis: Visualization and analysis tools

Author: Martin Haferanke
Date: 13.06.2025
"""

from menu.menu import run_movie_menu_loop
from movie_storage import storage_sql

from printers import print_title
from users.menu import run_user_menu_loop
from users.users import get_active_user_id

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
