# SQL Query Constants

# Movies

SQL_CREATE_MOVIES_TABLE = """
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL, 
    poster_url TEXT NOT NULL
)
"""

SQL_SELECT_MOVIES_BY_USER_ID = """
SELECT title, year, rating, poster_url 
FROM movies 
WHERE user_id = :user_id
"""

SQL_INSERT_MOVIE = """
INSERT INTO movies (user_id, title, year, rating, poster_url) 
VALUES (:user_id, :title, :year, :rating, :poster_url)
"""

SQL_DELETE_MOVIE = """
DELETE FROM movies 
WHERE title = :title AND user_id = :user_id
"""

SQL_UPDATE_MOVIE_RATING = """
UPDATE movies 
SET rating = :rating 
WHERE title = :title AND user_id = :user_id
"""


# Users

# SQL Queries related to the 'users' table

SQL_CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
)
"""

SQL_SELECT_ALL_USERS = """
SELECT id, username FROM users
"""

SQL_INSERT_USER_IF_NOT_EXISTS = """
INSERT OR IGNORE INTO users (username) VALUES (:username)
"""

SQL_SELECT_USER_BY_ID = """
SELECT username FROM users WHERE id = :user_id
"""
