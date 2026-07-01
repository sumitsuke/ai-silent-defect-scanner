def parse_int_field(data, key):
    # Check if the key exists in the dictionary
    if key in data:
        # Attempt to convert the value associated with the key to an integer
        try:
            return int(data[key])
        except ValueError:
            # Return None if conversion fails (e.g., non-numeric value)
            return None
    else:
        # Return None if the key does not exist in the dictionary
        return None
