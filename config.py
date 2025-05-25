# ====================
# File Paths
# ====================
from colorama import Fore, Style


DATA_FILE = "data.json"
HISTOGRAM_FILE = "speed_histogram.png"
INTERACTIVE_MAP_FILE = "ships_map.html"

# ====================
# External URLs
# ====================
GOOGLE_MAPS_URL = "https://maps.google.com/"

# ====================
# CLI Styling (ANSI color codes)
# ====================
COLOR_INPUT = "light_magenta"
COLOR_TEXT = "cyan"
COLOR_MENU_OPTIONS = "light_blue"
COLOR_VALUES = "light_cyan"
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_TITLE = "yellow"
COLOR_SUB_TITLE = "light_yellow"

HISTOGRAM_WIDTH = 10
HISTOGRAM_HEIGHT = 6

# Padding width for aligned command display and formatting
LABEL_PADDING = 25
ASTERISK_COUNT = 10

RATING_BASE = 0
RATING_LIMIT = 10

FIRST_FILM_RELEASE = 1888

COLOR_MAP = {
    # Normal colors
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    # Bright colors
    "light_red": Style.BRIGHT + Fore.RED,
    "light_green": Style.BRIGHT + Fore.GREEN,
    "light_yellow": Style.BRIGHT + Fore.YELLOW,
    "light_blue": Style.BRIGHT + Fore.BLUE,
    "light_magenta": Style.BRIGHT + Fore.MAGENTA,
    "light_cyan": Style.BRIGHT + Fore.CYAN,
    "light_white": Style.BRIGHT + Fore.WHITE,
}
# ====================
# Menu, Selection and Range
# ====================

MENU_MIN_INDEX = 0
MENU_MAX_INDEX = 10
