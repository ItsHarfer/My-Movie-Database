from config import DATA_FILE
from menu import run_menu_loop
from movie_storage import get_movie_list
from printers import print_title


def main() -> None:
    print_title("My movie database - Part 2")
    movie_data = get_movie_list(DATA_FILE)
    run_menu_loop(movie_data)


if __name__ == "__main__":
    main()
