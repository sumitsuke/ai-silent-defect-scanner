def parse_int_field(data, key):
    # Check if the key exists in the dictionary and if its value is an integer
    if key in data and isinstance(data[key], int):
        return data[key]
    else:
        raise ValueError(f"Key '{key}' not found or not an integer.")
