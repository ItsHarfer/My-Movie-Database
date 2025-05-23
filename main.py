from config import ASTERISK_COUNT, DATA_FILE
from menu import run_menu_loop
from movie_storage import get_data_from_file, save_movies
from printers import print_title


def main() -> None:
    """
    Entry point for the Movie App.
    """
    print_title("My movie database", ASTERISK_COUNT)
    movie_data = get_data_from_file(DATA_FILE)
    run_menu_loop(movie_data)


if __name__ == "__main__":
    main()
