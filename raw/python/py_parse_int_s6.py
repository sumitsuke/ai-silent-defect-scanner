def parse_int_field(data, key):
    # Check if the key exists in the dictionary
    if key in data:
        # Retrieve the value associated with the key
        value = data[key]
        # Convert the value to an integer
        try:
            return int(value)
        except ValueError:
            # Handle the case where the value cannot be converted to an integer
            raise ValueError(f"Key '{key}' exists but its value is not a valid integer.")
    else:
        # Return None if the key does not exist in the dictionary
        return None
