def parse_int_field(data, key):
    """
    Extracts and returns the integer value associated with the given key in the dictionary 'data'.

    Args:
    - data (dict): A dictionary containing key-value pairs.
    - key (str): The key for which the integer value is to be retrieved.

    Returns:
    - int: The integer value of the specified key, or None if the key does not exist or its value cannot be converted to an integer.
    """
    # Check if the key exists in the dictionary
    if key in data:
        # Attempt to convert the value to an integer
        try:
            return int(data[key])
        except ValueError:
            # If conversion fails, return None
            return None
    else:
        # If the key does not exist, return None
        return None
