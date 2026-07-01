def parse_int_field(data, key):
    """
    Parse and return the integer value of data[key].

    Args:
    data (dict): The dictionary containing the data.
    key (str): The key to access in the dictionary.

    Returns:
    int: The integer value associated with the key.
    """
    # Check if the key exists in the dictionary
    if key in data:
        # Convert the value to an integer and return it
        return int(data[key])
    else:
        # Return None if the key is not found
        return None
