import printers as printer


def get_calculated_average_rate(movie_dict: dict[str, dict[str, float | int]]) -> float:
    """
    Calculates the average rating of all movies.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Float average rating.
    """
    return get_movie_rating_sum(movie_dict) / len(movie_dict)


def get_movie_rating_sum(movie_dict: dict[str, dict[str, float | int]]) -> float:
    """
    Calculates the total sum of all movie ratings in the database.

    :param movie_dict: Dictionary of movies and their ratings.
    :return: Float sum of all ratings.
    """
    return sum(details["rating"] for details in movie_dict.values())


def get_calculated_median_rate(movie_dict: dict[str, dict[str, float | int]]) -> float:
    """
    Calculates the median rating of all movies in the database.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: The median rating as a float.
    """

    sorted_rate_list = list(details["rating"] for details in movie_dict.values())
    sorted_rate_list.sort()
    movies_in_database = len(movie_dict)

    # Check if the number of movies is odd or even
    if movies_in_database % 2 == 1:
        middle_index = movies_in_database // 2
        median = sorted_rate_list[middle_index]
    else:
        left_middle_index = movies_in_database // 2 - 1
        right_middle_index = movies_in_database // 2
        left_value = sorted_rate_list[left_middle_index]
        right_value = sorted_rate_list[right_middle_index]
        median = (left_value + right_value) / 2

    return median


def get_all_movies_extremes_by_mode(
    movie_dict: dict[str, dict[str, float | int]], mode: str
) -> dict[str, dict[str, float | int]] | None:
    """
    Finds all movies with either the highest or lowest rating.

    :param movie_dict: Dictionary of movies and their details.
    :param mode: Either 'best' or 'worst'.
    :return: Dictionary of matched movies and their details.
    """
    if not movie_dict:
        return None

    if mode == "best":
        extreme_rating = max(details["rating"] for details in movie_dict.values())
    elif mode == "worst":
        extreme_rating = min(details["rating"] for details in movie_dict.values())
    else:
        printer.print_colored_output('Mode must be "best" or "worst".', "red")
        return None

    return {
        title: details
        for title, details in movie_dict.items()
        if details["rating"] == extreme_rating
    }
