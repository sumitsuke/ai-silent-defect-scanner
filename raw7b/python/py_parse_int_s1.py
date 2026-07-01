def parse_int_field(data, key):
    """
    Extracts and converts the value associated with the specified key from a dictionary to an integer.

    Args:
        data (dict): The dictionary containing the data.
        key (str): The key whose value needs to be extracted and converted.

    Returns:
        int: The integer value of the data[key] if it can be successfully converted, otherwise None.
    """
    try:
        # Attempt to extract the value from the dictionary
        value = data.get(key)
        
        # Convert the value to an integer
        if value is not None:
            return int(value)
    
    except (KeyError, ValueError):
        # If the key does not exist or conversion fails, return None
        pass
    
    return None

# Example usage:
data = {
    "age": "30",
    "height": "180cm"
}

print(parse_int_field(data, "age"))  # Output: 30
print(parse_int_field(data, "height"))  # Output: None (because 'height' is not an integer)
print(parse_int_field(data, "weight"))  # Output: None (because 'weight' key does not exist)
