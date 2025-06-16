"""
storage_sql.py

Provides SQL-based storage utilities for managing users in the Movie Database application.

This module establishes a connection to the SQLite database, ensures that the users table exists,
and provides helper functions to interact with the user records, including listing users,
inserting new users, and retrieving users by ID.

Author: Martin Haferanke
Date: 13.06.2025
"""

from sqlalchemy import create_engine, text

from config.sql_queries import (
    SQL_CREATE_USERS_TABLE,
    SQL_SELECT_ALL_USERS,
    SQL_INSERT_USER_IF_NOT_EXISTS,
    SQL_SELECT_USER_BY_ID,
)

# Define the database URL
DB_URL = "sqlite:///data/movies.db"


# Create the engine
engine = create_engine(DB_URL, echo=False)


# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text(SQL_CREATE_USERS_TABLE))
    connection.commit()


def list_users() -> dict[int, dict[str, str]]:
    """
    Retrieves all users stored in the SQL database.

    :return: Dictionary mapping user IDs to dictionaries containing usernames.
             Example: {1: {"username": "Alice"}, 2: {"username": "Bob"}}
    """
    with engine.connect() as connection:
        result = connection.execute(text(SQL_SELECT_ALL_USERS))
        users = result.fetchall()

    return {row[0]: {"username": row[1]} for row in users}


def create_user_if_not_exists(username: str) -> None:
    """
    Inserts a new user into the database if they do not already exist.

    :param username: The name of the user to insert.
    :return: None
    """
    with engine.connect() as connection:
        connection.execute(
            text(SQL_INSERT_USER_IF_NOT_EXISTS),
            {"username": username},
        )
        connection.commit()


def get_user_by_id(user_id: int) -> str | None:
    """
    Retrieves a username from the database by user ID.

    :param user_id: The ID of the user to retrieve.
    :return: Username as a string if found, otherwise None.
    """
    with engine.connect() as connection:
        result = connection.execute(text(SQL_SELECT_USER_BY_ID), {"user_id": user_id})
        user = result.fetchone()
        return user[0] if user else None
