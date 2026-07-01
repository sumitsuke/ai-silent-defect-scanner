def parse_int_field(data, key):
    """
    Extract and return the integer value associated with the given key from the dictionary.

    Parameters:
    - data (dict): A dictionary containing data.
    - key (str): The key in the dictionary whose value is to be parsed as an integer.

    Returns:
    int: The integer value of the data[key].

    Example:
    >>> parse_int_field({'age': '25'}, 'age')
    25
    """
    if key in data and isinstance(data[key], str):
        return int(data[key])
    else:
        raise ValueError(f"Key '{key}' not found or does not contain an integer value.")
