import printers as printer


def get_calculated_average_rate(movie_dict: dict[str, float]) -> float:
    """
    Calculates the average rating of all movies.

    :param movie_dict: Dictionary of movies and ratings.
    :return: Float average rating.
    """
    movies_in_database = len(movie_dict)
    rating_sum = get_movie_rating_sum(movie_dict)
    average_rate = rating_sum / movies_in_database
    return average_rate


def get_movie_rating_sum(movie_dict: dict[str, float]) -> float:
    """
    Calculates the total sum of all movie ratings in the database.

    :param movie_dict: Dictionary of movies and their ratings.
    :return: Float sum of all ratings.
    """
    return sum(movie_dict.values())


def get_calculated_median_rate(movie_dict: dict[str, float]) -> float:
    """
    Calculates the median rating of all movies in the database.

    :param movie_dict: Dictionary of movie titles and their ratings.
    :return: The median rating as a float.
    """
    sorted_rate_list = list(movie_dict.values())
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


def get_all_movies_extremes_by_mode(movie_dict: dict[str, float], mode: str) -> dict[str, float] | None:
    """
    Finds all movies with either the highest or lowest rating.

    :param movie_dict: Dictionary of movies and ratings.
    :param mode: Either 'best' or 'worst'.
    :return: Dictionary of matched movies and their ratings.
    """
    if mode == 'best':
        movie = max(movie_dict, key=movie_dict.get)
    elif mode == 'worst':
        movie = min(movie_dict, key=movie_dict.get)
    else:
        printer.print_colored_output('Mode must be "best" or "worst".', 'red')
        return None

    all_movies = {}
    movie_rating = movie_dict[movie]

    # Add all movies that have the same rating as the best/worst movie
    for movie, rating in movie_dict.items():
        if movie_rating == rating:
            all_movies[movie] = rating

    return all_movies
