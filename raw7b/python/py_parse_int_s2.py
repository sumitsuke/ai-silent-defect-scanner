def parse_int_field(data, key):
    """
    Parses an integer field from the given dictionary.

    Args:
    data (dict): The dictionary containing the data.
    key (str): The key for which to extract the integer value.

    Returns:
    int: The integer value of the specified key. If the key does not exist or is not a valid integer, returns 0.
    """
    try:
        return int(data[key])
    except (KeyError, ValueError):
        return 0
