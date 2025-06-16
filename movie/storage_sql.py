"""
storage_sql.py

Provides SQL-based persistence for the Movie Database application.

This module manages all database interactions related to movies, including:
- Initializing the SQLite database and creating required tables
- Executing CRUD operations (create, read, update, delete) per user
- Validating user context to ensure proper access control
- Displaying user-specific success and error messages via colored CLI output

All records are stored per user and include metadata such as rating, year, and poster URL.
SQLAlchemy is used as the database toolkit.

Author: Martin Haferanke
Date: 06.06.2025
"""

from sqlalchemy import create_engine, text

from config.config import COLOR_ERROR, COLOR_SUCCESS
from config.sql_queries import (
    SQL_CREATE_MOVIES_TABLE,
    SQL_SELECT_MOVIES_BY_USER_ID,
    SQL_INSERT_MOVIE,
    SQL_DELETE_MOVIE,
    SQL_UPDATE_MOVIE,
)
from printers import print_colored_output
from users.session_user import get_active_user

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text(SQL_CREATE_MOVIES_TABLE))
    connection.commit()


def list_movies(user_id: int):
    """
    Retrieves all movies stored in the SQL database and returns them as a dictionary.

    :return: Dictionary of movie titles with associated year, rating, and poster URL.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(SQL_SELECT_MOVIES_BY_USER_ID),
            {"user_id": user_id},
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "note": row[3],
            "poster_url": row[4],
            "imdb_id": row[5],
            "country": row[6],
            "is_favorite": bool(row[7]),
        }
        for row in movies
    }


def add_movie(
    user_id: int, new_movie_title: str, attributes: dict[str, float | int]
) -> None:
    """
    Adds a new movie record to the SQL database with the provided attributes.

    :param user_id:
    :param new_movie_title: Title of the movie to be added.
    :param attributes: Dictionary containing "year", "rating", and "poster_url".
    :return: None. Prints a success or error message.
    """
    try:
        username = get_active_user()
        with engine.connect() as connection:
            connection.execute(
                text(SQL_INSERT_MOVIE),
                {
                    "user_id": user_id,
                    "title": new_movie_title,
                    "year": attributes["year"],
                    "rating": attributes["rating"],
                    "note": "",
                    "poster_url": attributes["poster_url"],
                    "imdb_id": attributes["imdb_id"],
                    "country": attributes["country"],
                    "is_favorite": False,
                },
            )
            connection.commit()

        return print_colored_output(
            f'✅ "{new_movie_title}" successfully added to {username}\'s (uId:{user_id}) collection.',
            COLOR_SUCCESS,
        )
    except Exception as e:
        return print_colored_output(f"❌ Error: {e}", COLOR_ERROR)


def delete_movie(user_id, title):
    """
    Deletes a movie entry from the SQL database based on its title.

    :param user_id:
    :param title: The title of the movie to delete.
    :return: None. Prints a success or error message.
    """
    with engine.connect() as connection:
        try:
            username = get_active_user()
            params = {"title": title, "user_id": user_id}
            connection.execute(text(SQL_DELETE_MOVIE), params)
            connection.commit()
            print_colored_output(
                f"✅ Movie '{title}' successfully deleted from {username}'s (uId:{user_id}) collection.",
                COLOR_SUCCESS,
            )
        except Exception as e:
            print_colored_output(f"❌ Error: {e}", COLOR_ERROR)


def update_movie(user_id, title, note, is_favorite):
    """
    Updates the note of an existing movie in the SQL database.


    :param user_id: ID of the user who owns the movie.
    :param title: Title of the movie to update.
    :param note: New note to associate with the movie.
    :param is_favorite: Boolean is indicating whether the movie is a favorite.
    :return: None. Prints a success or error message.
    """
    with engine.connect() as connection:
        try:
            username = get_active_user()
            params = {
                "title": title,
                "note": note,
                "user_id": user_id,
                "is_favorite": is_favorite,
            }
            connection.execute(text(SQL_UPDATE_MOVIE), params)
            connection.commit()
            print_colored_output(
                f"✅ Movie '{title}' successfully updated in {username}'s (uId:{user_id}) collection.",
                COLOR_SUCCESS,
            )
        except Exception as e:
            print_colored_output(f"❌ Error: {e}", COLOR_ERROR)
