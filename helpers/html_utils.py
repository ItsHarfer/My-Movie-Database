"""
helpers / html_utils.py

Generates and manipulates HTML content for visualizing movies data in a web-friendly format.

This module provides functions to dynamically inject movies-related content into HTML templates.
It supports placeholder replacement, movies card serialization, and country flag generation,
enabling consistent visual presentation of movies entries.

Functions:
- replace_placeholder_with_html_content: Replaces placeholders in HTML templates with actual content.
- generate_movie_html_content: Builds an HTML list of movies entries from a dictionary.
- serialize_movie: Transforms a movies dictionary into an HTML card.
- generate_movie_card: Produces styled HTML markup for an individual movies.
- extract_country_codes (imported): Converts country names to ISO codes for flag display.

These utilities allow seamless integration of backend movies data with frontend HTML output.

Author: Martin Haferanke
Date: 16.06.2025
"""

from config.config import COLOR_ERROR
from helpers.movie_utils import extract_country_codes
from printers import print_colored_output


def replace_placeholder_with_html_content(
    html: str, placeholder: str, output: str
) -> str:
    """
    Replaces a placeholder string in the given HTML content with the specified output.

    This is typically used to inject dynamic content (e.g. movies title, movies grid)
    into a predefined HTML template.

    :param html: The original HTML string containing the placeholder.
    :param placeholder: The placeholder string to be replaced (e.g. {{__PLACEHOLDER_TITLE__}}).
    :param output: The string to replace the placeholder with.
    :return: HTML string with the placeholder replaced by the output.
    """

    if placeholder not in html:
        print_colored_output(
            f"❌ Error: Placeholder '{placeholder}' not found in HTML template.",
            COLOR_ERROR,
        )
        return html
    return html.replace(placeholder, output)


def generate_movie_html_content(movie_data: dict[str, dict]) -> str:
    """
    Generates HTML markup for a list of movies based on the given movies data.

    Iterates through each movies entry and serializes it into an HTML list item
    using the `serialize_movie` function, wrapping all items in an ordered list container.

    :param movie_data: Dictionary of movies titles and their corresponding attribute dictionaries.
    :return: HTML string containing the formatted movies cards.
    """
    output = ""
    output += '<ol class="movies-grid">'
    for title, details in movie_data.items():
        movie_dict = details.copy()
        movie_dict["title"] = title
        output += serialize_movie(movie_dict)
    output += "</ol>"
    return output


def serialize_movie(movie_obj: dict) -> str:
    """
    Serializes a movies dictionary into an HTML card string.

    Extracts the movies's title, year, rating, and poster URL and passes them to
    the `generate_movie_card` function to produce the final HTML markup.

    :param movie_obj: Dictionary containing the movies's attributes, including title, year, rating, and poster URL.
    :return: A string of HTML representing the serialized movies card.
    """
    title = movie_obj.get("title", "")
    year = movie_obj.get("year", "Unknown")
    rating = movie_obj.get("rating", "Unknown")
    note = movie_obj.get("note", "")
    poster_url = movie_obj.get("poster_url", "Unknown")
    imdb_id = movie_obj.get("imdb_id", "Unknown")
    imdb_url = f"https://www.imdb.com/title/{imdb_id}"
    country = movie_obj.get("country", "Unknown")
    is_favorite = movie_obj.get("is_favorite", False)
    return generate_movie_card(
        title, year, rating, note, poster_url, imdb_url, country, is_favorite
    )


def generate_movie_card(
    title: str,
    year: str | int,
    rating: str | float,
    note: str,
    poster_url: str,
    imdb_url: str,
    country: str,
    is_favorite: bool,
) -> str:
    """
    Generates an HTML list item representing a movies card.

    Formats the provided movies data into a styled HTML snippet.


    :param country: Country(s) of the movies.
    :param note: Users preferred note about the movies.
    :param title: The title of the movies.
    :param year: The release year of the movies.
    :param rating: The IMDb rating of the movies.
    :param poster_url: URL of the movies poster image.
    :param imdb_url: URL to the movies's IMDb page.
    :param is_favorite: Boolean is indicating whether the movies is a favorite.

    :return: HTML string for the movies card.
    """
    country_codes = extract_country_codes(country)
    poster_wrapper_classes = (
        "poster-wrapper favorite" if is_favorite else "poster-wrapper"
    )

    output = ""
    output += f"<li>\n"
    output += f'  <div class="movies">\n'
    output += f'    <div class="{poster_wrapper_classes}" title="{note}">\n'
    if is_favorite:
        output += f'      <span class="favorite-icon">&#x1F451;</span>\n'
    output += f'      <a href="{imdb_url}" target="_blank">\n'
    output += f'        <img class="movies-poster" src="{poster_url}" alt="{title}">\n'
    output += f"      </a>\n"
    output += f"    </div>\n"
    output += f'    <div class="movies-title">{title}</div>\n'
    for code in country_codes:
        output += f"""    <img 
                            class="movies-flag" 
                            src="https://flagcdn.com/16x12/{code.lower()}.png" 
                            srcset="https://flagcdn.com/32x24/{code.lower()}.png 2x, https://flagcdn.com/48x36/{code.lower()}.png 3x"
                            width="16" height="12" alt="{code.upper()}">\n"""
    output += f'    <div class="movies-year">{year}</div>\n'
    output += f'    <div class="movies-rating-stars" style="--rating:{rating}" title="{rating}/10"></div>\n'
    output += f"  </div>\n"
    output += f"</li>\n"
    return output
