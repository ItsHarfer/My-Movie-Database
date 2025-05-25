import movie_storage
from config import DATA_FILE
from menu import run_menu_loop
from printers import print_title


def main() -> None:
    print_title("My movie database - Part 2")
    movies_dict = movie_storage.get_movie_list(DATA_FILE)
    run_menu_loop(movies_dict)


if __name__ == "__main__":
    main()
3
