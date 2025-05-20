from config import ASTERISK_COUNT
from menu import run_menu_loop
from printers import print_title


def main() -> None:
    """
    Entry point for the Movie App.
    """
    # TODO Get Data from file not hard coded

    movies = {
        "Pulp Fiction": {"rating": 9.5, "release": 1994},
        "The Room": {"rating": 3.6, "release": 2003},
        "The Godfather": {"rating": 9.2, "release": 1972},
        "The Godfather: Part II": {"rating": 9.0, "release": 1974},
        "The Dark Knight": {"rating": 9.0, "release": 2008},
        "12 Angry Men": {"rating": 8.9, "release": 1957},
        "Everything Everywhere All At Once": {"rating": 3.6, "release": 2022},
        "Forrest Gump": {"rating": 8.8, "release": 1994},
        "Star Wars: Episode V": {"rating": 8.7, "release": 1980},
    }
    print_title("My movie database", ASTERISK_COUNT)
    run_menu_loop(movies)


if __name__ == "__main__":
    main()
