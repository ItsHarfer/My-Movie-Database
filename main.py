from config import ASTERISK_COUNT, MOVIES
from menu import run_menu_loop
from printers import print_title


def main() -> None:
    """
    Entry point for the Movie App.
    """
    print_title("My movie database", ASTERISK_COUNT)
    run_menu_loop(MOVIES)


if __name__ == "__main__":
    main()
