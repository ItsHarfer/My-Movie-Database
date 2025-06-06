"""
movie_storage_sql.py

Provides SQL-based persistence for the Movie Database application.

This module manages all database interactions related to movies, including
creating the database and table, and executing CRUD operations. It acts as
a backend interface for storing and modifying movie records.

Author: Martin Haferanke
Date: 06.06.2025
"""

from sqlalchemy import create_engine, text

from config import COLOR_ERROR, COLOR_SUCCESS
from printers import print_colored_output

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL, 
            poster_url TEXT NOT NULL
        )
    """
        )
    )
    connection.commit()


def list_movies():
    """
    Retrieves all movies stored in the SQL database and returns them as a dictionary.

    :return: Dictionary of movie titles with associated year, rating, and poster URL.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies")
        )
        movies = result.fetchall()

    return {
        # Build and return dict with title as key and year, rating and poster as values
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }


def add_movie(new_movie_title: str, attributes: dict[str, float | int]) -> None:
    """
    Adds a new movie record to the SQL database with the provided attributes.

    :param new_movie_title: Title of the movie to be added.
    :param attributes: Dictionary containing "year", "rating", and "poster_url".
    :return: None. Prints a success or error message.
    """
    try:
        # Also add the movie to the SQL database
        with engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"
                ),
                {
                    "title": new_movie_title,
                    "year": int(attributes.get("year", None)),
                    "rating": float(attributes.get("rating", None)),
                    "poster_url": attributes.get("poster_url", None),
                },
            )
            connection.commit()

        return print_colored_output(
            f'✅ "{new_movie_title}" successfully added to the database.', COLOR_SUCCESS
        )
    except Exception as e:
        return print_colored_output(f"❌ Error: {e}", COLOR_ERROR)


def delete_movie(title):
    """
    Deletes a movie entry from the SQL database based on its title.

    :param title: The title of the movie to delete.
    :return: None. Prints a success or error message.
    """
    with engine.connect() as connection:
        try:
            query = "DELETE FROM movies WHERE title = :title"
            params = {"title": title}
            connection.execute(text(query), params)
            connection.commit()
            print(f"Movie '{title}' successfully deleted.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """
    Updates the rating of an existing movie in the SQL database.

    :param title: Title of the movie to update.
    :param rating: New rating value to set.
    :return: None. Prints a success or error message.
    """
    with engine.connect() as connection:
        try:
            query = "UPDATE movies SET rating = :rating WHERE title = :title"
            params = {"title": title, "rating": rating}
            connection.execute(text(query), params)
            connection.commit()
            print(f"Movie '{title}' successfully updated.")
        except Exception as e:
            print(f"Error: {e}")
