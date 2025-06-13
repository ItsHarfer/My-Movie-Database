from colorama import Fore, Style

# ====================
# File Paths
# ====================
DATA_FILE = "data.json"
HISTOGRAM_FILE = "speed_histogram.png"
INTERACTIVE_MAP_FILE = "ships_map.html"
HTML_TEMPLATE_FILE = "_static/index_template.html"
HTML_OUTPUT_FILE = "_static/index.html"

# ====================
# External Resources
# ====================
GOOGLE_MAPS_URL = "https://maps.google.com/"

# ====================
# CLI Styling Configuration
# ====================
COLOR_INPUT = "light_magenta"
COLOR_TEXT = "cyan"
COLOR_MENU_OPTIONS = "light_blue"
COLOR_VALUES = "light_cyan"
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_TITLE = "yellow"
COLOR_SUB_TITLE = "light_yellow"

# Mapping of color names to colorama styles
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
# Histogram Configuration
# ====================
HISTOGRAM_WIDTH = 10
HISTOGRAM_HEIGHT = 6
LABEL_PADDING = 25

# ====================
# General Display Settings
# ====================
ASTERISK_COUNT = 10  # Used for visual emphasis in CLI

# ====================
# Rating / movie Settings
# ====================
RATING_BASE = 0
RATING_LIMIT = 10
FIRST_MOVIE_RELEASE = 1888

# ====================
# Menu Selection Limits
# ====================
MENU_MIN_INDEX = 0
MENU_MAX_INDEX = 12

USER_MENU_MIN_INDEX = 0

# Commands that require movies to be present in movie_dict
COMMANDS_REQUIRING_MOVIES = {1, 3, 4, 5, 6, 7, 8, 9, 10}

PLACEHOLDER_TITLE = "__TEMPLATE_TITLE__"
PLACEHOLDER_MOVIE_GRID = "__TEMPLATE_MOVIE_GRID__"
