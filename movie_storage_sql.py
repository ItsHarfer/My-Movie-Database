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
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies")
        )
        movies = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }


def add_movie(new_movie_title: str, attributes: dict[str, float | int]) -> None:
    """
    Adds a new movie with numeric attributes to the database and the local dictionary, if it doesn't already exist.

    :param new_movie_title: The title of the movie to be added.
    :param attributes: Dictionary of numeric attributes (e.g. {"rating": 8.5, "release": 1994}).
    :return: None
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
    """Delete a movie from the database."""
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
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            query = "UPDATE movies SET title = :title, rating = :rating WHERE title = :title"
            params = {"title": title, "rating": rating}
            connection.execute(text(query), params)
            connection.commit()
            print(f"Movie '{title}' successfully updated.")
        except Exception as e:
            print(f"Error: {e}")
