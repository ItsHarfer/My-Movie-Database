"""
main.py

My movie database part 2

Main entry point of the movie management application.

This script launches an interactive command-line interface that allows users to
manage a collection of movies stored in a JSON file. Users can view, add, update,
and delete movies, as well as analyze movie data through a statistics module.

Features:
- Menu-based navigation using `menu_dispatcher`
- Loads configuration from `config.py`
- Initializes and updates movie data via `movie_storage.py`
- Uses helper and handler modules for input and output operations
- Includes analysis functionality for ratings, releases, and trends

Required files:
- data.json: JSON file storing persistent movie data
- config.py: Configuration settings such as file paths
- movie_storage.py: Logic for reading and writing movie data
- handlers.py, helpers.py: Functions for user interaction and data formatting
- analysis.py: Module for analyzing and displaying movie statistics
- menu.py, menu_dispatcher.py: Menu definitions and logic for dispatching menu actions

Author: Martin Haferanke
Cohort Feb'25
Date: 25.05.2025

"""

import movie_storage
import movie_storage_sql
from menu import run_menu_loop
from printers import print_title


def main() -> None:
    print_title("My movie database - SQL Edition")
    # movies_dict = movie_storage.get_movie_list(DATA_FILE)
    movie_dict = movie_storage_sql.list_movies()
    run_menu_loop(movie_dict)


if __name__ == "__main__":
    main()
3
