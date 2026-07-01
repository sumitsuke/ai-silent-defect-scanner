def parse_int_field(data, key):
    # Attempt to retrieve the value associated with the given key from the dictionary
    value = data.get(key)
    
    # Check if the retrieved value is not None and can be converted to an integer
    if value is not None and isinstance(value, int):
        return value
    else:
        raise ValueError(f"The field '{key}' does not exist or cannot be parsed as an integer.")
